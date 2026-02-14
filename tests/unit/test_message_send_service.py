"""Tests for message send application service."""

from __future__ import annotations

from pathlib import Path

import pytest

from elsterctl.application.message_send import MessageSendRequest, MessageSendService
from elsterctl.infrastructure.eric.client import EricSubmitResult


class _FakeEricClient:
    def __init__(self) -> None:
        self.last_kwargs = None

    def send_xml_with_certificate(self, **kwargs):
        self.last_kwargs = kwargs
        return EricSubmitResult(
            result_code=0,
            transfer_ticket="transfer-ticket",
            eric_response_xml="<EricAntwort />",
            server_response_xml="<ServerAntwort />",
        )


def _write_file(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def test_message_send_service_requires_pin_env_var(tmp_path: Path, monkeypatch) -> None:
    xml_path = _write_file(
        tmp_path / "message.xml",
        "<TransferHeader><Testmerker>700000004</Testmerker></TransferHeader>",
    )
    cert_path = _write_file(tmp_path / "cert.pfx", "dummy")

    monkeypatch.delenv("ELSTER_CERT_PIN", raising=False)

    service = MessageSendService(eric_client_factory=_FakeEricClient)
    request = MessageSendRequest(
        xml_path=xml_path,
        certificate_path=cert_path,
        pin_env_var="ELSTER_CERT_PIN",
        data_type_version="TH11",
        transfer_mode="test",
        validate_before_send=True,
    )

    with pytest.raises(ValueError, match="Certificate PIN not set"):
        service.send(request)


def test_message_send_service_requires_testmerker_in_test_mode(
    tmp_path: Path,
    monkeypatch,
) -> None:
    xml_path = _write_file(tmp_path / "message.xml", "<TransferHeader></TransferHeader>")
    cert_path = _write_file(tmp_path / "cert.pfx", "dummy")

    monkeypatch.setenv("ELSTER_CERT_PIN", "1234")

    service = MessageSendService(eric_client_factory=_FakeEricClient)
    request = MessageSendRequest(
        xml_path=xml_path,
        certificate_path=cert_path,
        pin_env_var="ELSTER_CERT_PIN",
        data_type_version="TH11",
        transfer_mode="test",
        validate_before_send=True,
    )

    with pytest.raises(ValueError, match="Test transfer mode requires"):
        service.send(request)


def test_message_send_service_maps_eric_result(tmp_path: Path, monkeypatch) -> None:
    xml_path = _write_file(
        tmp_path / "message.xml",
        "<TransferHeader><Testmerker>700000004</Testmerker></TransferHeader>",
    )
    cert_path = _write_file(tmp_path / "cert.pfx", "dummy")

    monkeypatch.setenv("ELSTER_CERT_PIN", "1234")

    service = MessageSendService(eric_client_factory=_FakeEricClient)
    request = MessageSendRequest(
        xml_path=xml_path,
        certificate_path=cert_path,
        pin_env_var="ELSTER_CERT_PIN",
        data_type_version="TH11",
        transfer_mode="test",
        validate_before_send=False,
    )

    result = service.send(request)

    assert result.result_code == 0
    assert result.transfer_ticket == "transfer-ticket"
    assert "EricAntwort" in result.eric_response_xml
    assert "ServerAntwort" in result.server_response_xml
