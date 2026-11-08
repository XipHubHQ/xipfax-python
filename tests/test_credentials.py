"""The specs run with no credential in their environment."""

import os

import pytest

from tests import credentials


def test_the_environment_holds_no_credential() -> None:
    assert credentials.left() == [], "conftest.py strips each before any spec loads"


def test_strip_takes_a_key_a_token_and_the_xipfax_variables_and_keeps_the_rest(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("XIPFAX_API_KEY", "stand-in")
    monkeypatch.setenv("XIPFAX_TO", "+1 202 555 0143")
    monkeypatch.setenv("GITHUB_TOKEN", "stand-in")
    monkeypatch.setenv("PLAIN_SETTING", "kept")

    removed = credentials.strip()

    assert removed == ["GITHUB_TOKEN", "XIPFAX_API_KEY", "XIPFAX_TO"]
    assert os.environ.get("PLAIN_SETTING") == "kept"
