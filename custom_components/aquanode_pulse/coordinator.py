"""Data coordinator, event journal and local alerts for AquaNode Pulse."""

from __future__ import annotations

import logging
import time
from typing import Any

from homeassistant.components import persistent_notification
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
from .const import (
    CONF_AUTOMATIC_NOTIFICATIONS,
    CONF_DISPLAY_NAME,
    CONF_NOTIFICATION_DELAY,
    CONF_VOLTAGE_MINIMUM,
    DEFAULT_AUTOMATIC_NOTIFICATIONS,
    DEFAULT_NOTIFICATION_DELAY,
    DEFAULT_VOLTAGE_MINIMUM,
    EVENT_CONNECTION_LOST,
    EVENT_INTERRUPTION,
    EVENT_VOLTAGE_LOW,
    EVENT_VOLTAGE_RECOVERED,
    UPDATE_INTERVAL,
)
from .history import PulseHistory
from .interruptions import MAINTENANCE, NETWORK, POWER, InterruptionTracker

_LOGGER = logging.getLogger(__name__)

VOLTAGE_RECOVERY_HYSTERESIS = 3.0


class AquaNodePulseCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Poll one local API and turn transitions into persistent HA events."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        api: AquaNodePulseApi,
        history: PulseHistory,
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
        self.history = history
        self.serial = str(entry.unique_id or "")
        self.interruptions = InterruptionTracker()
        self._connection_notification_open = False
        self._maintenance_until = 0.0
        self.interruptions.restore_boot_count(
            history.last_boot_count(self.serial),
        )
        if pending := history.pending_connection(self.serial):
            now_monotonic = hass.loop.time()
            now_wall = time.time()
            self.interruptions.restore_offline(
                now_monotonic,
                now_wall,
                float(pending["started_at"]),
            )
            try:
                maintenance_until_wall = float(
                    pending.get("maintenance_until") or 0,
                )
            except (TypeError, ValueError):
                maintenance_until_wall = 0.0
            if maintenance_until_wall > now_wall:
                self._maintenance_until = (
                    now_monotonic + maintenance_until_wall - now_wall
                )

    @property
    def last_interruption(self) -> dict[str, Any] | None:
        """Return the last saved interruption for entities and diagnostics."""
        return self.history.last_interruption(self.serial)

    @property
    def display_name(self) -> str:
        """Return the local name selected in Home Assistant."""
        configured = str(
            self.config_entry.options.get(CONF_DISPLAY_NAME, ""),
        ).strip()
        if configured:
            return configured
        if self.config_entry.title:
            return self.config_entry.title
        if self.data:
            return str(self.data.get("name") or "AquaNode Pulse")
        return "AquaNode Pulse"

    def suppress_connection_alerts(self, seconds: float = 45.0) -> None:
        """Silence the expected disconnect caused by a local restart/update."""
        self._maintenance_until = max(
            self._maintenance_until,
            self.hass.loop.time() + max(0.0, seconds),
        )
        self.async_update_listeners()

    @property
    def in_maintenance(self) -> bool:
        """Return whether a user-requested local restart is still expected."""
        return self.hass.loop.time() <= self._maintenance_until

    def _notifications_enabled(self) -> bool:
        return bool(
            self.config_entry.options.get(
                CONF_AUTOMATIC_NOTIFICATIONS,
                DEFAULT_AUTOMATIC_NOTIFICATIONS,
            ),
        )

    def _notification_delay(self) -> float:
        try:
            return max(
                0.0,
                float(
                    self.config_entry.options.get(
                        CONF_NOTIFICATION_DELAY,
                        DEFAULT_NOTIFICATION_DELAY,
                    ),
                ),
            )
        except (TypeError, ValueError):
            return DEFAULT_NOTIFICATION_DELAY

    def _voltage_minimum(self) -> float:
        try:
            return max(
                0.0,
                float(
                    self.config_entry.options.get(
                        CONF_VOLTAGE_MINIMUM,
                        DEFAULT_VOLTAGE_MINIMUM,
                    ),
                ),
            )
        except (TypeError, ValueError):
            return DEFAULT_VOLTAGE_MINIMUM

    def _is_romanian(self) -> bool:
        return str(self.hass.config.language or "").lower().startswith("ro")

    def _name(self, data: dict[str, Any] | None = None) -> str:
        return self.display_name

    def send_test_notification(self) -> None:
        """Create one local notification so setup can be checked safely."""
        if self._is_romanian():
            title = "Test AquaNode Pulse"
            message = f"Notificările locale pentru {self.display_name} funcționează."
        else:
            title = "AquaNode Pulse test"
            message = f"Local notifications for {self.display_name} are working."
        self._notify("test", title, message)

    def _notification_id(self, suffix: str) -> str:
        safe_serial = self.serial.lower().replace("-", "_")
        return f"aquanode_pulse_{safe_serial}_{suffix}"

    def _notify(self, suffix: str, title: str, message: str) -> None:
        persistent_notification.async_create(
            self.hass,
            message,
            title=title,
            notification_id=self._notification_id(suffix),
        )

    def _dismiss(self, suffix: str) -> None:
        persistent_notification.async_dismiss(
            self.hass,
            self._notification_id(suffix),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        now_monotonic = self.hass.loop.time()
        now_wall = time.time()
        try:
            data = await self.api.async_status()
        except AquaNodePulseInvalidAuth as err:
            raise ConfigEntryAuthFailed from err
        except AquaNodePulseCannotConnect as err:
            await self._async_handle_poll_failed(now_monotonic, now_wall)
            raise UpdateFailed(
                "AquaNode Pulse nu răspunde în rețeaua locală",
            ) from err
        except AquaNodePulseApiError as err:
            await self._async_handle_poll_failed(now_monotonic, now_wall)
            raise UpdateFailed(str(err)) from err

        interruption = self.interruptions.poll_succeeded(
            now_monotonic,
            data,
            now_wall,
        )
        if interruption is not None:
            await self._async_handle_recovery(
                data,
                interruption,
                now_monotonic,
            )

        self.history.record_boot_count(self.serial, data.get("boot_count"))
        await self._async_process_voltage(data, now_wall)
        return data

    async def _async_handle_poll_failed(
        self,
        now_monotonic: float,
        now_wall: float,
    ) -> None:
        first_failure = self.interruptions.poll_failed(
            now_monotonic,
            now_wall,
        )
        maintenance = now_monotonic <= self._maintenance_until
        if first_failure:
            maintenance_until_wall = (
                now_wall + max(0.0, self._maintenance_until - now_monotonic)
                if maintenance
                else None
            )
            await self.history.async_start_connection_loss(
                self.serial,
                started_at=now_wall,
                maintenance_until=maintenance_until_wall,
            )
            self.hass.bus.async_fire(
                EVENT_CONNECTION_LOST,
                {
                    "device_id": self.serial,
                    "name": self._name(),
                    "started_at": now_wall,
                    "entry_id": self.config_entry.entry_id,
                    "maintenance": maintenance,
                },
            )

        if (
            maintenance
            or self._connection_notification_open
            or not self._notifications_enabled()
            or self.interruptions.offline_seconds(now_monotonic)
            < self._notification_delay()
        ):
            return

        name = self._name()
        if self._is_romanian():
            title = "Posibilă pană de curent"
            message = (
                f"{name} nu mai răspunde. Poate fi o pană de curent sau o "
                "problemă de rețea. Cauza va fi confirmată la reconectare."
            )
        else:
            title = "Possible power outage"
            message = (
                f"{name} stopped responding. This may be a power outage or a "
                "network problem. The cause will be confirmed on reconnect."
            )
        self._notify("connection", title, message)
        self._connection_notification_open = True

    async def _async_handle_recovery(
        self,
        data: dict[str, Any],
        interruption,
        now_monotonic: float,
    ) -> None:
        pending = self.history.pending_connection(self.serial)
        try:
            persisted_maintenance_until = float(
                (pending or {}).get("maintenance_until") or 0,
            )
        except (TypeError, ValueError):
            persisted_maintenance_until = 0.0
        maintenance = (
            now_monotonic <= self._maintenance_until
            or interruption.ended_at <= persisted_maintenance_until
        )
        cause = MAINTENANCE if maintenance else interruption.cause
        event = await self.history.async_add_interruption(
            self.serial,
            cause=cause,
            started_at=interruption.started_at,
            ended_at=interruption.ended_at,
            duration_seconds=interruption.duration_seconds,
        )
        self.interruptions.last.cause = cause

        _LOGGER.info(
            "%s: %s interruption lasting %.1fs",
            self.serial,
            cause,
            interruption.duration_seconds,
        )
        self.hass.bus.async_fire(
            EVENT_INTERRUPTION,
            {
                "device_id": self.serial,
                "name": data.get("name"),
                "cause": cause,
                "started_at": event["started_at"],
                "ended_at": event["ended_at"],
                "duration_seconds": event["duration_seconds"],
                "entry_id": self.config_entry.entry_id,
            },
        )

        if maintenance:
            self._dismiss("connection")
            self._connection_notification_open = False
            return

        should_notify = (
            self._notifications_enabled()
            and interruption.duration_seconds >= self._notification_delay()
        )
        if not should_notify:
            self._dismiss("connection")
            self._connection_notification_open = False
            return

        name = self._name(data)
        duration = _short_duration(
            interruption.duration_seconds,
            self._is_romanian(),
        )
        if self._is_romanian():
            if cause == POWER:
                title = "Curentul a revenit"
                message = f"{name} confirmă o pană de curent de {duration}."
            elif cause == NETWORK:
                title = "Conexiunea a revenit"
                message = (
                    f"{name} a rămas alimentat. A fost o problemă de rețea "
                    f"de {duration}."
                )
            else:
                title = "Dispozitivul a revenit"
                message = (
                    f"{name} răspunde din nou după {duration}. Cauza nu a "
                    "putut fi stabilită sigur."
                )
        else:
            if cause == POWER:
                title = "Power is back"
                message = f"{name} confirms a power outage lasting {duration}."
            elif cause == NETWORK:
                title = "Connection restored"
                message = (
                    f"{name} stayed powered. This was a network problem "
                    f"lasting {duration}."
                )
            else:
                title = "Device is back"
                message = (
                    f"{name} is responding again after {duration}. The cause "
                    "could not be confirmed."
                )
        self._notify("connection", title, message)
        self._connection_notification_open = False

    async def _async_process_voltage(
        self,
        data: dict[str, Any],
        now_wall: float,
    ) -> None:
        voltage = data.get("voltage", {})
        if not (
            voltage.get("ready")
            and voltage.get("sensor_present")
            and voltage.get("calibrated")
            and not voltage.get("clipped")
        ):
            return
        try:
            value = float(voltage.get("voltage_v"))
        except (TypeError, ValueError):
            return
        if value <= 0:
            return

        self.history.record_voltage(self.serial, now_wall, value)
        threshold = self._voltage_minimum()
        open_incident = self.history.open_voltage_incident(self.serial)

        if threshold > 0 and value < threshold:
            if open_incident is None:
                event = await self.history.async_start_voltage_incident(
                    self.serial,
                    started_at=now_wall,
                    voltage=value,
                    threshold=threshold,
                )
                self.hass.bus.async_fire(
                    EVENT_VOLTAGE_LOW,
                    {
                        "device_id": self.serial,
                        "name": data.get("name"),
                        "voltage": value,
                        "threshold": threshold,
                        "started_at": event["started_at"],
                        "entry_id": self.config_entry.entry_id,
                    },
                )
                if self._notifications_enabled():
                    if self._is_romanian():
                        self._notify(
                            "voltage",
                            "Tensiune scăzută",
                            f"{self._name(data)} măsoară {value:.1f} V, sub "
                            f"limita de {threshold:.1f} V.",
                        )
                    else:
                        self._notify(
                            "voltage",
                            "Low voltage",
                            f"{self._name(data)} measures {value:.1f} V, below "
                            f"the {threshold:.1f} V limit.",
                        )
            else:
                self.history.update_voltage_incident(self.serial, value)
            return

        if open_incident is None:
            return
        if threshold > 0 and value < threshold + VOLTAGE_RECOVERY_HYSTERESIS:
            return

        event = await self.history.async_close_voltage_incident(
            self.serial,
            ended_at=now_wall,
            voltage=value,
        )
        if event is None:
            return
        self.hass.bus.async_fire(
            EVENT_VOLTAGE_RECOVERED,
            {
                "device_id": self.serial,
                "name": data.get("name"),
                "voltage": value,
                "threshold": event["threshold_voltage"],
                "started_at": event["started_at"],
                "ended_at": event["ended_at"],
                "duration_seconds": event["duration_seconds"],
                "minimum_voltage": event["minimum_voltage"],
                "entry_id": self.config_entry.entry_id,
            },
        )
        if self._notifications_enabled():
            duration = _short_duration(
                float(event["duration_seconds"]),
                self._is_romanian(),
            )
            if self._is_romanian():
                self._notify(
                    "voltage",
                    "Tensiunea a revenit",
                    f"{self._name(data)} măsoară din nou {value:.1f} V. "
                    f"Incidentul a durat {duration}.",
                )
            else:
                self._notify(
                    "voltage",
                    "Voltage recovered",
                    f"{self._name(data)} now measures {value:.1f} V. "
                    f"The incident lasted {duration}.",
                )


def _short_duration(seconds: float, romanian: bool) -> str:
    value = max(0, round(seconds))
    if value < 60:
        return f"{value} sec"
    if value < 3_600:
        minutes = max(1, round(value / 60))
        return f"{minutes} min"
    hours = value / 3_600
    suffix = "h"
    return f"{hours:.1f} {suffix}".replace(".0 ", " ")
