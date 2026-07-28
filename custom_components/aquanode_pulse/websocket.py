"""WebSocket commands used by the bundled AquaNode Pulse dashboard."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback

from .const import DATA_HISTORY, DOMAIN
from .history import PERIODS, PulseHistory


def _history(hass: HomeAssistant) -> PulseHistory:
    return hass.data[DOMAIN][DATA_HISTORY]


def _configured(hass: HomeAssistant, serial: str) -> bool:
    return any(
        entry.unique_id == serial for entry in hass.config_entries.async_entries(DOMAIN)
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): "aquanode_pulse/history",
        vol.Required("serial"): str,
        vol.Optional("period", default="week"): vol.In(PERIODS),
    }
)
@callback
def websocket_history(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return persistent voltage samples and events for one board."""
    serial = msg["serial"].upper()
    if not _configured(hass, serial):
        connection.send_error(
            msg["id"],
            "device_not_found",
            "AquaNode Pulse device is not configured",
        )
        return
    connection.send_result(
        msg["id"],
        _history(hass).payload(serial, msg["period"]),
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): "aquanode_pulse/clear_history",
        vol.Required("serial"): str,
    }
)
@websocket_api.require_admin
@websocket_api.async_response
async def websocket_clear_history(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Clear one device journal after an explicit dashboard confirmation."""
    serial = msg["serial"].upper()
    if not _configured(hass, serial):
        connection.send_error(
            msg["id"],
            "device_not_found",
            "AquaNode Pulse device is not configured",
        )
        return
    await _history(hass).async_clear_events(serial)
    connection.send_result(msg["id"], {"ok": True})


def async_register(hass: HomeAssistant) -> None:
    """Register both commands once for the integration."""
    websocket_api.async_register_command(hass, websocket_history)
    websocket_api.async_register_command(hass, websocket_clear_history)
