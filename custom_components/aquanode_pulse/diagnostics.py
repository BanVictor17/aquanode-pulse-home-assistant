"""Downloadable diagnostics for AquaNode Pulse."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from .const import CONF_PASSWORD

TO_REDACT = {CONF_PASSWORD}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry,
) -> dict[str, Any]:
    """Return useful state without leaking the label password."""
    coordinator = entry.runtime_data.coordinator
    history = coordinator.history.payload(coordinator.serial, "year")
    return {
        "config_entry": async_redact_data(dict(entry.data), TO_REDACT),
        "options": dict(entry.options),
        "device": coordinator.data,
        "last_update_success": coordinator.last_update_success,
        "local_polling": coordinator.poll_diagnostics,
        "history": {
            "saved_event_count": history["saved_event_count"],
            "power_outage_count": history["power_outage_count"],
            "year_voltage_points": len(history["voltage"]),
            "last_voltage": history["last_voltage"],
            "pending_connection": coordinator.history.pending_connection(
                coordinator.serial,
            ),
        },
    }
