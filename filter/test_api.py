"""Tests for the JSON dashboard API foundation."""

from __future__ import annotations

import os
import sqlite3
import tempfile
import time

os.environ.setdefault("STATE_DIR", tempfile.mkdtemp(prefix="sf_api_test_"))

import dashboard  # noqa: E402
import filter as f  # noqa: E402


def _seed(tmp_path, monkeypatch):
    monkeypatch.setenv("DASHBOARD_USER", "admin")
    monkeypatch.setenv("DASHBOARD_PASSWORD", "secret")
    monkeypatch.delenv("DASHBOARD_USERS", raising=False)
    db_path = tmp_path / "spamfilter.db"
    config_path = tmp_path / "accounts.yml"
    config_path.write_text(
        "accounts:\n"
        "  - name: acct\n"
        "    imap_host: imap.example.com\n"
        "    user: user@example.com\n"
        "    password_encrypted: enc:v1:test-token\n"
        "    mode: shadow\n"
        "  - name: other\n"
        "    imap_host: imap2.example.com\n"
        "    user: other@example.com\n"
        "    password_encrypted: enc:v1:other-test-token\n"
    )
    monkeypatch.setattr(dashboard, "DB_PATH", db_path)
    monkeypatch.setattr(dashboard, "CONFIG_PATH", config_path)
    monkeypatch.setattr(dashboard, "_rspamd_stats", lambda: {"scanned": 10})
    with sqlite3.connect(db_path) as conn:
        conn.executescript(f.SCHEMA)
        now = int(time.time())
        conn.executemany(
            "INSERT INTO events(account, ts, message_id, event, detail) "
            "VALUES(?,?,?,?,?)",
            [
                ("acct", now - 90, "msg-1", "scan", "score=9.20 mode=shadow"),
                ("acct", now - 70, "msg-1", "learn_spam", "grace_elapsed"),
                ("other", now - 50, "msg-2", "scan", "score=1.10 mode=shadow"),
            ],
        )
        conn.executemany(
            "INSERT INTO messages(account, message_id, first_seen, last_seen, "
            "current_folder, our_score, our_action, learned_as, sender, "
            "subject, received_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            [
                ("acct", "msg-1", now - 100, now - 90, "Junk", 9.2,
                 "shadow", "spam", "bad@example.com", "Spam", now - 100),
                ("other", "msg-2", now - 60, now - 50, "INBOX", 1.1,
                 None, None, "ok@example.com", "Ham", now - 60),
            ],
        )
        conn.execute(
            "INSERT INTO safe_mode(account, scope, entered_at, reason) "
            "VALUES(?,?,?,?)",
            ("acct", "learning", now - 30, "test"),
        )
    return dashboard.app.test_client()


def _login(client):
    return client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "secret"},
    )


def test_api_protected_routes_return_json_401(tmp_path, monkeypatch):
    client = _seed(tmp_path, monkeypatch)
    resp = client.get("/api/messages")
    assert resp.status_code == 401
    assert resp.get_json() == {"error": "unauthorized"}


def test_api_me_anonymous(tmp_path, monkeypatch):
    client = _seed(tmp_path, monkeypatch)
    resp = client.get("/api/auth/me")
    assert resp.status_code == 200
    assert resp.get_json() == {"authenticated": False}


def test_api_login_invalid_credentials(tmp_path, monkeypatch):
    client = _seed(tmp_path, monkeypatch)
    resp = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "wrong"},
    )
    assert resp.status_code == 401
    assert resp.get_json() == {"error": "invalid_credentials"}


def test_api_login_and_me(tmp_path, monkeypatch):
    client = _seed(tmp_path, monkeypatch)
    resp = _login(client)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["authenticated"] is True
    assert data["is_admin"] is True
    assert data["csrf_token"]

    resp = client.get("/api/auth/me")
    assert resp.status_code == 200
    assert resp.get_json()["user"] == "admin"


def test_api_logout_clears_session(tmp_path, monkeypatch):
    client = _seed(tmp_path, monkeypatch)
    _login(client)
    resp = client.post("/api/auth/logout")
    assert resp.status_code == 200
    assert resp.get_json() == {"authenticated": False}

    resp = client.get("/api/messages")
    assert resp.status_code == 401


def test_api_accounts_masks_passwords(tmp_path, monkeypatch):
    client = _seed(tmp_path, monkeypatch)
    _login(client)
    resp = client.get("/api/accounts")
    assert resp.status_code == 200
    items = resp.get_json()["items"]
    configured = {item["name"]: item["configured"] for item in items}
    assert configured["acct"]["password_set"] is True
    assert "password" not in configured["acct"]
    assert "password_encrypted" not in configured["acct"]


def test_api_read_endpoints_return_seeded_data(tmp_path, monkeypatch):
    client = _seed(tmp_path, monkeypatch)
    _login(client)
    for path in (
        "/api/summary",
        "/api/messages",
        "/api/events",
        "/api/learned",
        "/api/safe-mode",
        "/api/rspamd/stats",
    ):
        resp = client.get(path)
        assert resp.status_code == 200, path
        assert resp.is_json, path


def test_api_messages_rejects_invalid_band(tmp_path, monkeypatch):
    client = _seed(tmp_path, monkeypatch)
    _login(client)
    resp = client.get("/api/messages?band=bad")
    assert resp.status_code == 400
    assert resp.get_json() == {"error": "invalid_band"}


def test_api_messages_account_filter_allowed_and_forbidden(tmp_path, monkeypatch):
    client = _seed(tmp_path, monkeypatch)

    def scoped_users():
        return {
            "member": dashboard._User(
                "member", "plain:ignored", False, frozenset({"acct"})
            )
        }

    monkeypatch.setattr(dashboard, "_load_users", scoped_users)
    with client.session_transaction() as sess:
        sess["user"] = "member"

    resp = client.get("/api/messages?account=acct")
    assert resp.status_code == 200
    assert {item["account"] for item in resp.get_json()["items"]} == {"acct"}

    resp = client.get("/api/messages?account=other")
    assert resp.status_code == 403
    assert resp.get_json() == {"error": "forbidden_account"}


def test_api_respects_scoped_user(tmp_path, monkeypatch):
    client = _seed(tmp_path, monkeypatch)

    def scoped_users():
        return {
            "member": dashboard._User(
                "member", "plain:ignored", False, frozenset({"acct"})
            )
        }

    monkeypatch.setattr(dashboard, "_load_users", scoped_users)
    with client.session_transaction() as sess:
        sess["user"] = "member"

    resp = client.get("/api/messages")
    assert resp.status_code == 200
    assert {item["account"] for item in resp.get_json()["items"]} == {"acct"}

    resp = client.get("/api/accounts")
    assert resp.status_code == 200
    assert {item["name"] for item in resp.get_json()["items"]} == {"acct"}

    resp = client.get("/api/rspamd/stats")
    assert resp.status_code == 403
