"""Data coordinator for AquaNode Pulse."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    AquaNodePulseApi,
    AquaNodePulseApiError,
    AquaNodePulseCannotConnect,
    AquaNodePulseInvalidAuth,
)
from .const import UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class AquaNodePulseCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Poll one local API once for every group of entities."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        api: AquaNodePulseApi,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=f"AquaNode Pulse {entry.unique_id}",
            update_interval=UPDATE_INTERVAL,
            always_update=False,
        )
        self.api = api

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self.api.async_status()
        except AquaNodePulseInvalidAuth as err:
            raise ConfigEntryAuthFailed from err
        except AquaNodePulseCannotConnect as err:
            raise UpdateFailed("AquaNode Pulse nu răspunde în rețeaua locală") from err
        except AquaNodePulseApiError as err:
            raise UpdateFailed(str(err)) from err
