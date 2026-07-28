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
from .const import DOMAIN, EVENT_INTERRUPTION, UPDATE_INTERVAL
from .interruptions import InterruptionTracker

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
        self.interruptions = InterruptionTracker()

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            data = await self.api.async_status()
        except AquaNodePulseInvalidAuth as err:
            raise ConfigEntryAuthFailed from err
        except AquaNodePulseCannotConnect as err:
            # A wrong password is not an interruption; an unreachable board is.
            self.interruptions.poll_failed(self.hass.loop.time())
            raise UpdateFailed("AquaNode Pulse nu răspunde în rețeaua locală") from err
        except AquaNodePulseApiError as err:
            self.interruptions.poll_failed(self.hass.loop.time())
            raise UpdateFailed(str(err)) from err

        if (
            interruption := self.interruptions.poll_succeeded(
                self.hass.loop.time(), data
            )
        ) is not None:
            # Fired rather than only stored, because during the interruption
            # every entity of this device is unavailable and an automation has
            # nothing to trigger on. The event arrives the moment contact is
            # restored and says what it was.
            _LOGGER.info(
                "%s: %s interruption lasting %.0fs",
                data.get("serial"),
                interruption.cause,
                interruption.duration_seconds,
            )
            self.hass.bus.async_fire(
                EVENT_INTERRUPTION,
                {
                    "device_id": data.get("serial"),
                    "name": data.get("name"),
                    "cause": interruption.cause,
                    "duration_seconds": round(interruption.duration_seconds),
                    "entry_id": self.config_entry.entry_id,
                },
            )
        return data
