"""Persistent local history for the AquaNode Pulse dashboard.

Live values still come directly from the board every second. This store keeps
the information that must survive a Home Assistant restart:

* classified power/network interruptions;
* low-voltage incidents;
* multi-resolution voltage aggregates for the four dashboard periods;
* the last boot counter and last valid voltage reading.

Writing one JSON row every second would wear storage and grow without bound.
Voltage is therefore aggregated into minute, 15-minute and six-hour buckets.
That preserves useful min/average/max graphs for 24 hours, 7/30 days and one
year while keeping the file small.
"""

from __future__ import annotations

import math
import time
from copy import deepcopy
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

STORAGE_KEY = "aquanode_pulse.history"
STORAGE_VERSION = 1
SAVE_DELAY_SECONDS = 5
EVENT_RETENTION_SECONDS = 400 * 24 * 60 * 60
MAX_EVENTS_PER_DEVICE = 2_000
HISTORY_FORMAT = 2
LEGACY_TRANSIENT_MAX_SECONDS = 2.5

SERIES = {
    "minute": (60, 26 * 60 * 60),
    "quarter_hour": (15 * 60, 32 * 24 * 60 * 60),
    "six_hour": (6 * 60 * 60, 370 * 24 * 60 * 60),
}

PERIODS = {
    "day": ("minute", 24 * 60 * 60),
    "week": ("quarter_hour", 7 * 24 * 60 * 60),
    "month": ("quarter_hour", 30 * 24 * 60 * 60),
    "year": ("six_hour", 365 * 24 * 60 * 60),
}

INTERRUPTION_KINDS = {"power", "network", "unknown", "maintenance"}


def _is_legacy_transient_network_event(event: Any) -> bool:
    """Identify only the old two-second poll artifacts, not proven Wi-Fi loss."""
    if not isinstance(event, dict):
        return False
    if event.get("kind") != "network" or event.get("evidence"):
        return False
    try:
        duration = float(event.get("duration_seconds"))
    except (TypeError, ValueError):
        return False
    return 0 <= duration <= LEGACY_TRANSIENT_MAX_SECONDS


def add_to_bucket(
    rows: list[dict[str, Any]],
    at: float,
    value: float,
    bucket_seconds: int,
) -> bool:
    """Add one voltage sample and return True when a new bucket starts."""
    slot = int(at // bucket_seconds) * bucket_seconds
    if rows and rows[-1].get("at") == slot:
        row = rows[-1]
        count = max(1, int(row.get("count", 1)))
        row["minimum"] = round(min(float(row["minimum"]), value), 2)
        row["maximum"] = round(max(float(row["maximum"]), value), 2)
        row["average"] = round(
            (float(row["average"]) * count + value) / (count + 1),
            3,
        )
        row["count"] = count + 1
        return False

    rows.append(
        {
            "at": slot,
            "minimum": round(value, 2),
            "maximum": round(value, 2),
            "average": round(value, 3),
            "count": 1,
        }
    )
    return True


def prune_rows(
    rows: list[dict[str, Any]],
    cutoff: float,
) -> None:
    """Remove rows older than cutoff in-place."""
    first_kept = 0
    while first_kept < len(rows) and float(rows[first_kept].get("at", 0)) < cutoff:
        first_kept += 1
    if first_kept:
        del rows[:first_kept]


class PulseHistory:
    """One persistent history store shared by every configured Pulse."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self._store: Store[dict[str, Any]] = Store(
            hass,
            STORAGE_VERSION,
            STORAGE_KEY,
        )
        self.data: dict[str, Any] = {"devices": {}}
        self.loaded = False

    async def async_load(self) -> None:
        """Load and normalize the saved file once."""
        if self.loaded:
            return
        loaded = await self._store.async_load()
        if isinstance(loaded, dict) and isinstance(loaded.get("devices"), dict):
            self.data = loaded
        self.data.setdefault("devices", {})
        self.loaded = True
        migrated = False
        for device in self.data["devices"].values():
            if not isinstance(device, dict):
                continue
            if int(device.get("history_format") or 1) >= HISTORY_FORMAT:
                continue
            events = device.get("events")
            if isinstance(events, list):
                device["events"] = [
                    event
                    for event in events
                    if not _is_legacy_transient_network_event(event)
                ]
            device["history_format"] = HISTORY_FORMAT
            migrated = True
        if migrated:
            await self.async_save()

    def _device(self, serial: str) -> dict[str, Any]:
        devices = self.data.setdefault("devices", {})
        device = devices.setdefault(
            serial,
            {
                "events": [],
                "voltage": {name: [] for name in SERIES},
                "last_boot_count": None,
                "last_wifi_disconnect_count": None,
                "last_voltage": None,
                "pending_connection": None,
                "history_format": HISTORY_FORMAT,
            },
        )
        device.setdefault("events", [])
        voltage = device.setdefault("voltage", {})
        for name in SERIES:
            voltage.setdefault(name, [])
        device.setdefault("last_boot_count", None)
        device.setdefault("last_wifi_disconnect_count", None)
        device.setdefault("last_voltage", None)
        device.setdefault("pending_connection", None)
        device.setdefault("history_format", HISTORY_FORMAT)
        return device

    def last_boot_count(self, serial: str) -> int | None:
        """Return the persisted boot counter used to classify reconnects."""
        value = self._device(serial).get("last_boot_count")
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    def record_boot_count(self, serial: str, value: Any) -> None:
        """Persist a changed boot counter without writing every poll."""
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            return
        device = self._device(serial)
        if device.get("last_boot_count") == parsed:
            return
        device["last_boot_count"] = parsed
        self._schedule_save()

    def last_wifi_disconnect_count(self, serial: str) -> int | None:
        """Return the last per-boot Wi-Fi disconnect count."""
        value = self._device(serial).get("last_wifi_disconnect_count")
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    def record_wifi_disconnect_count(self, serial: str, value: Any) -> None:
        """Persist changed Wi-Fi evidence without writing every poll."""
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            return
        device = self._device(serial)
        if device.get("last_wifi_disconnect_count") == parsed:
            return
        device["last_wifi_disconnect_count"] = parsed
        self._schedule_save()

    def record_voltage(self, serial: str, at: float, value: Any) -> None:
        """Aggregate one calibrated voltage measurement."""
        try:
            parsed = float(value)
        except (TypeError, ValueError):
            return
        if not math.isfinite(parsed) or parsed <= 0:
            return

        device = self._device(serial)
        device["last_voltage"] = {
            "at": round(at, 3),
            "value": round(parsed, 2),
        }

        started_new_minute = False
        for name, (bucket_seconds, retention_seconds) in SERIES.items():
            rows = device["voltage"][name]
            created = add_to_bucket(rows, at, parsed, bucket_seconds)
            prune_rows(rows, at - retention_seconds)
            if name == "minute":
                started_new_minute = created

        # The active minute is updated in memory every second. Persist when a
        # new minute begins, so at most the unfinished minute is lost on a hard
        # Home Assistant shutdown.
        if started_new_minute:
            self._schedule_save()

    def last_voltage(self, serial: str) -> dict[str, Any] | None:
        """Return the last valid calibrated reading."""
        value = self._device(serial).get("last_voltage")
        return deepcopy(value) if isinstance(value, dict) else None

    def pending_connection(self, serial: str) -> dict[str, Any] | None:
        """Return a contact loss that has not ended yet."""
        value = self._device(serial).get("pending_connection")
        return deepcopy(value) if isinstance(value, dict) else None

    async def async_start_connection_loss(
        self,
        serial: str,
        *,
        started_at: float,
        maintenance_until: float | None,
    ) -> dict[str, Any]:
        """Persist the start immediately so an HA restart cannot erase it."""
        device = self._device(serial)
        existing = device.get("pending_connection")
        if isinstance(existing, dict):
            return deepcopy(existing)
        pending = {
            "started_at": round(started_at, 3),
            "maintenance_until": (
                round(maintenance_until, 3) if maintenance_until is not None else None
            ),
        }
        device["pending_connection"] = pending
        await self.async_save()
        return deepcopy(pending)

    async def async_cancel_connection_loss(self, serial: str) -> None:
        """Discard a pending contact loss proven to be only a local poll gap."""
        device = self._device(serial)
        if device.get("pending_connection") is None:
            return
        device["pending_connection"] = None
        await self.async_save()

    async def async_add_interruption(
        self,
        serial: str,
        *,
        cause: str,
        started_at: float,
        ended_at: float,
        duration_seconds: float,
        evidence: str | None = None,
    ) -> dict[str, Any]:
        """Save one completed loss of contact."""
        event = {
            "id": f"connection-{int(ended_at * 1000)}",
            "kind": cause if cause in INTERRUPTION_KINDS else "unknown",
            "started_at": round(started_at, 3),
            "ended_at": round(ended_at, 3),
            "duration_seconds": round(max(0.0, duration_seconds), 3),
            "evidence": evidence,
        }
        self._device(serial)["pending_connection"] = None
        self._append_event(serial, event)
        await self.async_save()
        return event

    async def async_start_voltage_incident(
        self,
        serial: str,
        *,
        started_at: float,
        voltage: float,
        threshold: float,
    ) -> dict[str, Any]:
        """Open and persist a low-voltage incident."""
        existing = self.open_voltage_incident(serial)
        if existing is not None:
            return existing
        event = {
            "id": f"voltage-{int(started_at * 1000)}",
            "kind": "voltage",
            "started_at": round(started_at, 3),
            "ended_at": None,
            "duration_seconds": None,
            "minimum_voltage": round(voltage, 2),
            "restored_voltage": None,
            "threshold_voltage": round(threshold, 2),
        }
        self._append_event(serial, event)
        await self.async_save()
        return event

    def update_voltage_incident(self, serial: str, voltage: float) -> None:
        """Keep the minimum value of an open low-voltage incident."""
        event = self.open_voltage_incident(serial)
        if event is None:
            return
        current = float(event.get("minimum_voltage", voltage))
        if voltage >= current:
            return
        event["minimum_voltage"] = round(voltage, 2)
        self._schedule_save()

    async def async_close_voltage_incident(
        self,
        serial: str,
        *,
        ended_at: float,
        voltage: float,
    ) -> dict[str, Any] | None:
        """Resolve and persist the current low-voltage incident."""
        event = self.open_voltage_incident(serial)
        if event is None:
            return None
        event["ended_at"] = round(ended_at, 3)
        event["duration_seconds"] = round(
            max(0.0, ended_at - float(event["started_at"])),
            3,
        )
        event["restored_voltage"] = round(voltage, 2)
        await self.async_save()
        return deepcopy(event)

    def open_voltage_incident(self, serial: str) -> dict[str, Any] | None:
        """Return the active low-voltage incident, if there is one."""
        for event in reversed(self._device(serial)["events"]):
            if event.get("kind") == "voltage" and event.get("ended_at") is None:
                return event
        return None

    def last_interruption(self, serial: str) -> dict[str, Any] | None:
        """Return the latest classified connection interruption."""
        for event in reversed(self._device(serial)["events"]):
            if event.get("kind") in INTERRUPTION_KINDS:
                return deepcopy(event)
        return None

    def interruption_count(self, serial: str) -> int:
        """Count saved real power outages for the dashboard and entities."""
        return sum(
            event.get("kind") == "power" for event in self._device(serial)["events"]
        )

    def payload(self, serial: str, period: str) -> dict[str, Any]:
        """Build the bounded response consumed by the custom panel."""
        series_name, period_seconds = PERIODS.get(period, PERIODS["week"])
        now = time.time()
        cutoff = now - period_seconds
        device = self._device(serial)
        events = [
            deepcopy(event)
            for event in device["events"]
            if float(event.get("ended_at") or event.get("started_at") or 0) >= cutoff
        ]
        voltage = [
            deepcopy(row)
            for row in device["voltage"][series_name]
            if float(row.get("at", 0)) >= cutoff
        ]
        return {
            "serial": serial,
            "period": period,
            "from": round(cutoff, 3),
            "to": round(now, 3),
            "events": events,
            "recent_events": [deepcopy(event) for event in device["events"][-50:]],
            "voltage": voltage,
            "last_voltage": self.last_voltage(serial),
            "saved_event_count": len(device["events"]),
            "power_outage_count": self.interruption_count(serial),
        }

    async def async_clear_events(self, serial: str) -> None:
        """Clear completed events but keep graphs and active incidents."""
        device = self._device(serial)
        device["events"] = [
            event for event in device["events"] if event.get("ended_at") is None
        ]
        await self.async_save()

    def _append_event(self, serial: str, event: dict[str, Any]) -> None:
        device = self._device(serial)
        events = device["events"]
        events.append(event)
        cutoff = time.time() - EVENT_RETENTION_SECONDS
        device["events"] = [
            item
            for item in events[-MAX_EVENTS_PER_DEVICE:]
            if float(item.get("ended_at") or item.get("started_at") or 0) >= cutoff
        ]

    def _schedule_save(self) -> None:
        self._store.async_delay_save(self._data_to_save, SAVE_DELAY_SECONDS)

    def _data_to_save(self) -> dict[str, Any]:
        return self.data

    async def async_save(self) -> None:
        """Write current history immediately."""
        await self._store.async_save(self.data)
