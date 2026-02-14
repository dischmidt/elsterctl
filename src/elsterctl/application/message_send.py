"""Application service for sending a Sonstige Nachricht via ERiC."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from elsterctl.infrastructure.eric.client import EricClient, EricSubmitResult


@dataclass(frozen=True)
class MessageSendRequest:
    """Input data for message transmission."""

    xml_path: Path
    certificate_path: Path
    pin_env_var: str
    data_type_version: str
    transfer_mode: str
    validate_before_send: bool


@dataclass(frozen=True)
class MessageSendResult:
    """Result of a message transmission."""

    result_code: int
    transfer_ticket: str | None
    eric_response_xml: str
    server_response_xml: str


class MessageSendService:
    """Coordinates message send workflow between CLI and ERiC client."""

    def __init__(self, eric_client_factory: type[EricClient] = EricClient) -> None:
        self._eric_client_factory = eric_client_factory

    def send(self, request: MessageSendRequest) -> MessageSendResult:
        if not request.xml_path.exists():
            raise ValueError(f"XML file not found: {request.xml_path}")
        if not request.certificate_path.exists():
            raise ValueError(f"Certificate file not found: {request.certificate_path}")

        cert_pin = os.getenv(request.pin_env_var)
        if not cert_pin:
            raise ValueError(
                f"Certificate PIN not set. Export environment variable: {request.pin_env_var}"
            )

        xml_payload = request.xml_path.read_text(encoding="utf-8")

        if request.transfer_mode == "test" and "<Testmerker>" not in xml_payload:
            raise ValueError(
                "Test transfer mode requires a <Testmerker> in the XML transfer header."
            )

        eric_client = self._eric_client_factory()
        submit_result: EricSubmitResult = eric_client.send_xml_with_certificate(
            xml_payload=xml_payload,
            data_type_version=request.data_type_version,
            certificate_path=request.certificate_path,
            certificate_pin=cert_pin,
            validate_before_send=request.validate_before_send,
        )

        return MessageSendResult(
            result_code=submit_result.result_code,
            transfer_ticket=submit_result.transfer_ticket,
            eric_response_xml=submit_result.eric_response_xml,
            server_response_xml=submit_result.server_response_xml,
        )
