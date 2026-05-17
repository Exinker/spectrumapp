import pytest

from spectrumapp.windows.modifiers import close


def test_close(
    object_name: str,
    window,
    monkeypatch: pytest.MonkeyPatch,
    mocker,
):
    wrapped = mocker.Mock()
    monkeypatch.setattr('spectrumapp.windows.modifiers.find_window', lambda *args, **kwargs: window)

    decorated = close(object_name)(wrapped)
    decorated()

    window.close_mock.assert_called_once_with()
    wrapped.assert_called_once_with()


def test_close_window_not_found(
    object_name: str,
    monkeypatch: pytest.MonkeyPatch,
    mocker,
):
    wrapped = mocker.Mock()
    monkeypatch.setattr('spectrumapp.windows.modifiers.find_window', lambda *args, **kwargs: None)

    decorated = close(object_name)(wrapped)
    decorated()

    wrapped.assert_called_once_with()
