"""Tests for account configuration safety checks."""

from __future__ import annotations

import os
import tempfile

import pytest

os.environ.setdefault("STATE_DIR", tempfile.mkdtemp(prefix="sf_config_test_"))

import filter as f  # noqa: E402


def _encrypted_password(monkeypatch, password: str = "secret") -> str:
    key = f.generate_secret_key()
    monkeypatch.setenv(f.SECRET_KEY_ENV, key)
    return f.encrypt_config_secret(password)


def _write_config(tmp_path, monkeypatch, extra: str = ""):
    path = tmp_path / "accounts.yml"
    password = _encrypted_password(monkeypatch)
    path.write_text(
        "accounts:\n"
        "  - name: acct\n"
        "    imap_host: imap.example.com\n"
        "    user: user@example.com\n"
        f"    password_encrypted: {password}\n"
        f"{extra}"
    )
    return path


def test_load_accounts_decrypts_password_and_defaults_to_tls(tmp_path, monkeypatch):
    accounts = f.load_accounts(_write_config(tmp_path, monkeypatch))
    assert len(accounts) == 1
    assert accounts[0].password == "secret"
    assert accounts[0].ssl is True
    assert accounts[0].imap_port == 993


def test_load_accounts_rejects_ssl_false_before_imap_login(tmp_path, monkeypatch):
    path = _write_config(tmp_path, monkeypatch, "    ssl: false\n    imap_port: 143\n")
    with pytest.raises(SystemExit) as ex:
        f.load_accounts(path)
    assert "ssl=false is not supported" in str(ex.value)
    assert "credentials" in str(ex.value)


def test_load_accounts_rejects_plaintext_password(tmp_path, monkeypatch):
    monkeypatch.setenv(f.SECRET_KEY_ENV, f.generate_secret_key())
    path = tmp_path / "accounts.yml"
    path.write_text(
        "accounts:\n"
        "  - name: acct\n"
        "    imap_host: imap.example.com\n"
        "    user: user@example.com\n"
        "    password: secret\n"
    )
    with pytest.raises(SystemExit) as ex:
        f.load_accounts(path)
    assert "plaintext password is not supported" in str(ex.value)


def test_load_accounts_requires_secret_key_for_encrypted_password(tmp_path, monkeypatch):
    encrypted = _encrypted_password(monkeypatch)
    monkeypatch.delenv(f.SECRET_KEY_ENV, raising=False)
    path = tmp_path / "accounts.yml"
    path.write_text(
        "accounts:\n"
        "  - name: acct\n"
        "    imap_host: imap.example.com\n"
        "    user: user@example.com\n"
        f"    password_encrypted: {encrypted}\n"
    )
    with pytest.raises(SystemExit) as ex:
        f.load_accounts(path)
    assert f.SECRET_KEY_ENV in str(ex.value)


def test_load_accounts_reads_secret_key_from_state_file(tmp_path, monkeypatch):
    key = f.generate_secret_key()
    key_path = tmp_path / "azkaspam.secret_key"
    key_path.write_text(key)
    monkeypatch.delenv(f.SECRET_KEY_ENV, raising=False)
    monkeypatch.setattr(f, "SECRET_KEY_PATH", key_path)
    password = f.encrypt_config_secret("from-file")
    path = tmp_path / "accounts.yml"
    path.write_text(
        "accounts:\n"
        "  - name: acct\n"
        "    imap_host: imap.example.com\n"
        "    user: user@example.com\n"
        f"    password_encrypted: {password}\n"
    )
    accounts = f.load_accounts(path)
    assert accounts[0].password == "from-file"


def test_load_accounts_rejects_invalid_encrypted_password(tmp_path, monkeypatch):
    monkeypatch.setenv(f.SECRET_KEY_ENV, f.generate_secret_key())
    path = tmp_path / "accounts.yml"
    path.write_text(
        "accounts:\n"
        "  - name: acct\n"
        "    imap_host: imap.example.com\n"
        "    user: user@example.com\n"
        "    password_encrypted: enc:v1:not-a-valid-token\n"
    )
    with pytest.raises(SystemExit) as ex:
        f.load_accounts(path)
    assert "could not be decrypted" in str(ex.value)
