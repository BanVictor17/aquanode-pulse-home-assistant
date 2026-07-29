"""Small async client for the local AquaNode Pulse API."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from aiohttp import (
    ClientConnectionError,
    ClientError,
    ClientResponse,
    ClientSession,
    ClientTimeout,
    ConnectionTimeoutError,
    SocketTimeoutError,
)

from .const import (
    REQUEST_CONNECT_TIMEOUT_SECONDS,
    REQUEST_RESPONSE_TIMEOUT_SECONDS,
)


class AquaNodePulseApiError(Exception):
    """Base error raised by the local API client."""


class AquaNodePulseCannotConnect(AquaNodePulseApiError):
    """A connection to the device could not be established or was lost."""


class AquaNodePulseResponseTimeout(AquaNodePulseApiError):
    """The device stayed reachable but its local HTTP response stalled."""


class AquaNodePulseInvalidAuth(AquaNodePulseApiError):
    """The label password was rejected."""


class AquaNodePulseInvalidResponse(AquaNodePulseApiError):
    """The device answered with an unexpected payload."""


class AquaNodePulseApi:
    """Communicate directly with one Pulse device over the LAN."""

    def __init__(
        self,
        session: ClientSession,
        host: str,
        port: int,
        password: str,
    ) -> None:
        self._session = session
        self.host = host
        self.port = port
        self._password = password

    @property
    def base_url(self) -> str:
        """Return the local device URL."""
        host = f"[{self.host}]" if ":" in self.host else self.host
        return f"http://{host}:{self.port}"

    async def async_info(self) -> dict[str, Any]:
        """Read public identity information used during discovery."""
        return await self._async_request("GET", "/api/v1/info", authenticated=False)

    async def async_status(self) -> dict[str, Any]:
        """Read all local measurements with one request."""
        payload = await self._async_request("GET", "/api/v1/status")
        if payload.get("api_version") != 1 or not payload.get("serial"):
            raise AquaNodePulseInvalidResponse("missing identity")
        return payload

    async def async_set_idle_led(self, enabled: bool) -> None:
        """Enable or disable the steady online LED."""
        await self._async_request(
            "POST",
            "/api/v1/settings",
            json={"idle_led_on": enabled},
        )

    async def async_calibrate_voltage(self, reference_voltage: float) -> None:
        """Calibrate the local voltage scale against a true-RMS reference."""
        await self._async_request(
            "POST",
            "/api/v1/calibration",
            json={"reference_voltage": reference_voltage},
        )

    async def async_reset_voltage_calibration(self) -> None:
        """Remove the local voltage calibration."""
        await self._async_request("DELETE", "/api/v1/calibration")

    async def async_identify(self) -> None:
        """Blink the device LED."""
        await self._async_request("POST", "/api/v1/actions/identify")

    async def async_restart(self) -> None:
        """Restart the device cleanly."""
        await self._async_request("POST", "/api/v1/actions/restart")

    async def _async_request(
        self,
        method: str,
        path: str,
        *,
        authenticated: bool = True,
        json: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        headers = (
            {"Authorization": f"Bearer {self._password}"} if authenticated else None
        )
        try:
            # Keep connection and response timeouts separate. A failed TCP
            # connection is evidence that the board is unreachable; a socket
            # read timeout can also happen while its cooperative HTTP server is
            # briefly busy even though Wi-Fi and MQTT remain connected.
            timeout = ClientTimeout(
                total=None,
                sock_connect=REQUEST_CONNECT_TIMEOUT_SECONDS,
                sock_read=REQUEST_RESPONSE_TIMEOUT_SECONDS,
            )
            async with self._session.request(
                method,
                f"{self.base_url}{path}",
                headers=headers,
                json=json,
                timeout=timeout,
            ) as response:
                return await self._async_decode(response)
        except AquaNodePulseApiError:
            raise
        except ConnectionTimeoutError as err:
            raise AquaNodePulseCannotConnect("connection_timeout") from err
        except SocketTimeoutError as err:
            raise AquaNodePulseResponseTimeout("response_timeout") from err
        except ClientConnectionError as err:
            raise AquaNodePulseCannotConnect(type(err).__name__) from err
        except TimeoutError as err:
            # Defensive fallback for older aiohttp builds which did not expose
            # the more specific socket timeout subclass.
            raise AquaNodePulseResponseTimeout("response_timeout") from err
        except (ClientError, OSError) as err:
            raise AquaNodePulseCannotConnect from err

    async def _async_decode(self, response: ClientResponse) -> dict[str, Any]:
        if response.status == 401:
            await response.read()
            raise AquaNodePulseInvalidAuth
        try:
            payload = await response.json(content_type=None)
        except ClientConnectionError:
            raise
        except (ValueError, ClientError) as err:
            raise AquaNodePulseInvalidResponse from err
        if response.status >= 400:
            error = payload.get("error", f"http_{response.status}")
            raise AquaNodePulseApiError(str(error))
        if not isinstance(payload, dict):
            raise AquaNodePulseInvalidResponse("JSON object expected")
        return payload
