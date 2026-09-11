"""Tests for account configuration safety checks."""

from __future__ import annotations

import os
import tempfile

import pytest

os.environ.setdefault("STATE_DIR", tempfile.mkdtemp(prefix="sf_config_test_"))

import filter as f  # noqa: E402


def _write_config(tmp_path, extra: str = ""):
    path = tmp_path / "accounts.yml"
    path.write_text(
        "accounts:\n"
        "  - name: acct\n"
        "    imap_host: imap.example.com\n"
        "    user: user@example.com\n"
        "    password: secret\n"
        f"{extra}"
    )
    return path


def test_load_accounts_defaults_to_tls(tmp_path):
    accounts = f.load_accounts(_write_config(tmp_path))
    assert len(accounts) == 1
    assert accounts[0].ssl is True
    assert accounts[0].imap_port == 993


def test_load_accounts_rejects_ssl_false_before_imap_login(tmp_path):
    path = _write_config(tmp_path, "    ssl: false\n    imap_port: 143\n")
    with pytest.raises(SystemExit) as ex:
        f.load_accounts(path)
    assert "ssl=false is not supported" in str(ex.value)
    assert "credentials" in str(ex.value)
