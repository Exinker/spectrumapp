import pytest
from pydantic import SecretStr

from spectrumapp.configs import TELEGRAM_CONFIG


def test_dump_remote_button_enabled(
    token: str,
    chat_id: str,
    create_dump_remote_button,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(TELEGRAM_CONFIG, 'token', SecretStr(token))
    monkeypatch.setattr(TELEGRAM_CONFIG, 'chat_id', chat_id)

    button = create_dump_remote_button()
    assert button.isEnabled()


def test_dump_remote_button_disabled_without_telegram_token(
    chat_id: str,
    create_dump_remote_button,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(TELEGRAM_CONFIG, 'token', SecretStr(''))
    monkeypatch.setattr(TELEGRAM_CONFIG, 'chat_id', chat_id)

    button = create_dump_remote_button()
    assert not button.isEnabled()


def test_dump_remote_button_disabled_without_telegram_chat_id(
    token: str,
    create_dump_remote_button,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(TELEGRAM_CONFIG, 'token', SecretStr(token))
    monkeypatch.setattr(TELEGRAM_CONFIG, 'chat_id', '')

    button = create_dump_remote_button()
    assert not button.isEnabled()
