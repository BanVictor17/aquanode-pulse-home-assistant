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
    return {
        "config_entry": async_redact_data(dict(entry.data), TO_REDACT),
        "device": entry.runtime_data.coordinator.data,
        "last_update_success": entry.runtime_data.coordinator.last_update_success,
    }
