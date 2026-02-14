"""Python-facing ERiC client façade."""

from __future__ import annotations

import ctypes
import os
from dataclasses import dataclass
from pathlib import Path

from elsterctl.infrastructure.eric.bindings import EricBoundSymbols, configure_base_signatures
from elsterctl.infrastructure.eric.errors import EricProcessingError
from elsterctl.infrastructure.eric.loader import load_eric_library


@dataclass(frozen=True)
class EricSubmitResult:
    """Structured outcome of an ERiC submission operation."""

    result_code: int
    transfer_ticket: str | None
    eric_response_xml: str
    server_response_xml: str


class EricClient:
    """High-level client wrapping the ERiC C API."""

    ERIC_VALIDIERE = 1 << 1
    ERIC_SENDE = 1 << 2

    class _EricVerschluesselungsParameter(ctypes.Structure):
        _fields_ = [
            ("version", ctypes.c_uint32),
            ("zertifikatHandle", ctypes.c_uint32),
            ("pin", ctypes.c_char_p),
        ]

    def __init__(self) -> None:
        self._lib = load_eric_library()
        self._symbols: EricBoundSymbols = configure_base_signatures(self._lib)

    def initialize(self, *args: object) -> int:
        """Initialize ERiC runtime and return ERiC result code."""
        return int(self._symbols.initialize(*args))

    def process(self, *args: object) -> int:
        """Trigger ERiC processing and return ERiC result code."""
        return int(self._symbols.process(*args))

    def shutdown(self, *args: object) -> int:
        """Shutdown ERiC runtime and return ERiC result code."""
        return int(self._symbols.shutdown(*args))

    def send_xml_with_certificate(
        self,
        *,
        xml_payload: str,
        data_type_version: str,
        certificate_path: Path,
        certificate_pin: str,
        validate_before_send: bool,
    ) -> EricSubmitResult:
        """Submit XML payload via ERiC using certificate-based authentication.

        This implementation uses a compatibility call strategy because ERiC
        signatures differ between wrapper generations.
        """
        plugin_path = self._resolve_plugin_path()
        init_code = self.initialize(plugin_path, None)
        if init_code != 0:
            raise self._build_processing_error("ERiC initialization failed", init_code)

        process_code: int | None = None
        cert_handle: ctypes.c_int | None = None
        eric_response_buffer: ctypes.c_void_p | None = None
        server_response_buffer: ctypes.c_void_p | None = None
        try:
            cert_handle = self._get_certificate_handle(certificate_path)
            cert_params = self._EricVerschluesselungsParameter(
                version=3,
                zertifikatHandle=cert_handle.value,
                pin=certificate_pin.encode("utf-8"),
            )

            eric_response_buffer = self._create_response_buffer()
            server_response_buffer = self._create_response_buffer()

            flags = self.ERIC_SENDE | (self.ERIC_VALIDIERE if validate_before_send else 0)
            process_code = self._process_send(
                xml_payload=xml_payload,
                data_type_version=data_type_version,
                flags=flags,
                cert_params=ctypes.pointer(cert_params),
                eric_response_buffer=eric_response_buffer,
                server_response_buffer=server_response_buffer,
            )
            if process_code != 0:
                raise self._build_processing_error("ERiC processing failed", process_code)

            eric_response_xml = self._read_response_buffer(eric_response_buffer)
            server_response_xml = self._read_response_buffer(server_response_buffer)
        finally:
            if eric_response_buffer:
                self._free_response_buffer(eric_response_buffer)
            if server_response_buffer:
                self._free_response_buffer(server_response_buffer)
            if cert_handle is not None:
                self._close_certificate_handle(cert_handle)

            shutdown_code = self.shutdown()
            if shutdown_code != 0 and (process_code is None or process_code == 0):
                raise self._build_processing_error("ERiC shutdown failed", shutdown_code)

        return EricSubmitResult(
            result_code=process_code,
            transfer_ticket=None,
            eric_response_xml=eric_response_xml,
            server_response_xml=server_response_xml,
        )

    def _resolve_plugin_path(self) -> bytes:
        lib_path = os.getenv("ELSTER_ERIC_LIB")
        if not lib_path:
            raise EricProcessingError("ELSTER_ERIC_LIB is not set.", -1)

        lib_dir = Path(lib_path).resolve().parent
        if not lib_dir.exists():
            raise EricProcessingError(f"ERiC lib directory not found: {lib_dir}", -1)

        if (lib_dir / "plugins").exists() or (lib_dir / "plugins2").exists():
            return str(lib_dir).encode("utf-8")

        raise EricProcessingError(
            f"ERiC plugins directory not found under: {lib_dir} (expected plugins or plugins2)",
            -1,
        )

    def _get_certificate_handle(self, certificate_path: Path) -> ctypes.c_int:
        try:
            function = self._lib.EricGetHandleToCertificate
        except AttributeError as exc:
            raise EricProcessingError("Missing symbol EricGetHandleToCertificate.", -1) from exc

        function.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p]
        function.restype = ctypes.c_int

        cert_handle = ctypes.c_int()
        result_code = function(
            ctypes.pointer(cert_handle),
            None,
            str(certificate_path).encode("utf-8"),
        )
        if result_code != 0:
            raise self._build_processing_error("Could not open certificate handle", result_code)
        return cert_handle

    def _close_certificate_handle(self, cert_handle: ctypes.c_int) -> None:
        try:
            function = self._lib.EricCloseHandleToCertificate
        except AttributeError:
            return

        function.argtypes = [ctypes.c_int]
        function.restype = ctypes.c_int
        function(cert_handle)

    def _create_response_buffer(self) -> ctypes.c_void_p:
        try:
            function = self._lib.EricRueckgabepufferErzeugen
        except AttributeError as exc:
            raise EricProcessingError("Missing symbol EricRueckgabepufferErzeugen.", -1) from exc

        function.argtypes = []
        function.restype = ctypes.c_void_p
        return function()

    def _read_response_buffer(self, buffer: ctypes.c_void_p) -> str:
        try:
            function = self._lib.EricRueckgabepufferInhalt
        except AttributeError as exc:
            raise EricProcessingError("Missing symbol EricRueckgabepufferInhalt.", -1) from exc

        function.argtypes = [ctypes.c_void_p]
        function.restype = ctypes.c_char_p
        content = function(buffer)
        if not content:
            return ""
        return content.decode("utf-8", errors="replace")

    def _free_response_buffer(self, buffer: ctypes.c_void_p) -> None:
        try:
            function = self._lib.EricRueckgabepufferFreigeben
        except AttributeError:
            return

        function.argtypes = [ctypes.c_void_p]
        function.restype = ctypes.c_int
        function(buffer)

    def _process_send(
        self,
        *,
        xml_payload: str,
        data_type_version: str,
        flags: int,
        cert_params: ctypes.c_void_p,
        eric_response_buffer: ctypes.c_void_p,
        server_response_buffer: ctypes.c_void_p,
    ) -> int:
        process_function = self._symbols.process
        process_function.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_uint32,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_void_p,
        ]
        process_function.restype = ctypes.c_int

        return self.process(
            xml_payload.encode("utf-8"),
            data_type_version.encode("utf-8"),
            flags,
            None,
            cert_params,
            None,
            eric_response_buffer,
            server_response_buffer,
        )

    def _build_processing_error(self, prefix: str, result_code: int) -> EricProcessingError:
        details = self._resolve_error_text(result_code)
        if details:
            return EricProcessingError(f"{prefix}: {details}", result_code)
        return EricProcessingError(f"{prefix}.", result_code)

    def _resolve_error_text(self, result_code: int) -> str | None:
        try:
            function = self._lib.EricHoleFehlerText
        except AttributeError:
            return None

        buffer = None
        try:
            buffer = self._create_response_buffer()
            function.argtypes = [ctypes.c_int, ctypes.c_void_p]
            function.restype = ctypes.c_int
            text_result = function(result_code, buffer)
            if text_result != 0:
                return None

            message = self._read_response_buffer(buffer).strip()
            return message or None
        except EricProcessingError:
            return None
        finally:
            if buffer:
                self._free_response_buffer(buffer)

