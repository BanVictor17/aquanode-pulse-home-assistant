"""End-to-end setup and interruption checks against real Home Assistant."""

from __future__ import annotations

import time
from unittest.mock import AsyncMock, patch

import pytest
from aiohttp import ConnectionTimeoutError, SocketTimeoutError
from homeassistant.components import persistent_notification
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import CONF_HOST, STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.aquanode_pulse.api import (
    AquaNodePulseApi,
    AquaNodePulseCannotConnect,
    AquaNodePulseResponseTimeout,
)
from custom_components.aquanode_pulse.const import (
    CONF_PASSWORD,
    CONF_PORT,
    DOMAIN,
)
from custom_components.aquanode_pulse.history import PulseHistory

pytestmark = pytest.mark.usefixtures("enable_custom_integrations")

STATUS = {
    "api_version": 1,
    "serial": "AP-429385",
    "name": "AquaNode Pulse 429385",
    "model": "AquaNode Pulse",
    "firmware": "1.3.1",
    "uptime_s": 12_345,
    "boot_count": 8,
    "wifi": {
        "connected": True,
        "rssi_dbm": -58,
        "ip": "192.0.2.42",
        "disconnect_count": 0,
    },
    "cloud": {"connected": False},
    "voltage": {
        "ready": True,
        "sensor_present": True,
        "clipped": False,
        "raw_rms_mv": 420.0,
        "bias_mv": 1_650,
        "calibrated": True,
        "calibration_factor": 0.55,
        "voltage_v": 231.0,
    },
    "settings": {"idle_led_on": True},
    "diagnostics": {
        "free_heap_bytes": 170_000,
        "max_alloc_heap_bytes": 90_000,
    },
}


def _metrics(hass: HomeAssistant) -> dict:
    return {
        state.attributes["aquanode_metric"]: state
        for state in hass.states.async_all()
        if state.attributes.get("aquanode_pulse")
    }


@pytest.mark.asyncio
async def test_setup_short_outage_and_power_recovery(
    hass: HomeAssistant,
    mock_async_zeroconf,
) -> None:
    """Load every platform, retain a failed poll and classify the reboot."""
    assert mock_async_zeroconf is not None
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: "192.0.2.42",
            CONF_PORT: 6053,
            CONF_PASSWORD: "test-password",
        },
        title="Acasă",
        unique_id="AP-429385",
    )
    entry.add_to_hass(hass)

    status = AsyncMock(return_value=STATUS)
    with patch(
        "custom_components.aquanode_pulse.api.AquaNodePulseApi.async_status",
        status,
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        assert entry.state is ConfigEntryState.LOADED

        metrics = _metrics(hass)
        assert {
            "automatic_notifications",
            "calibration_reference",
            "diagnostic_logging",
            "display_name",
            "last_interruption_started",
            "last_voltage",
            "local_connection",
            "notification_delay",
            "router_on_ups",
            "test_notification",
            "voltage",
            "voltage_minimum",
        } <= metrics.keys()
        assert metrics["local_connection"].state == STATE_ON
        assert metrics["voltage"].state == "231.0"

        coordinator = entry.runtime_data.coordinator
        status.side_effect = AquaNodePulseCannotConnect()
        await coordinator.async_refresh()
        await hass.async_block_till_done()

        # One failed TCP connection is only a candidate. The local ESP32 HTTP
        # server can miss one request without Wi-Fi or mains going away.
        assert _metrics(hass)["local_connection"].state == STATE_ON
        assert entry.runtime_data.history.pending_connection("AP-429385") is None

        await coordinator.async_refresh()
        await hass.async_block_till_done()

        assert _metrics(hass)["local_connection"].state == STATE_OFF
        pending = entry.runtime_data.history.pending_connection("AP-429385")
        assert pending is not None
        assert pending["started_at"] > 0
        notification = persistent_notification._async_get_or_create_notifications(
            hass,
        ).get("aquanode_pulse_ap_429385_connection")
        assert notification is not None
        assert notification["title"] == "Possible power outage"

        status.side_effect = None
        status.return_value = {
            **STATUS,
            "uptime_s": 2,
            "boot_count": 9,
        }
        await coordinator.async_refresh()
        await hass.async_block_till_done()

        assert _metrics(hass)["local_connection"].state == STATE_ON
        assert entry.runtime_data.history.pending_connection("AP-429385") is None
        interruption = entry.runtime_data.history.last_interruption("AP-429385")
        assert interruption is not None
        assert interruption["kind"] == "power"
        assert interruption["started_at"] <= interruption["ended_at"]
        notification = persistent_notification._async_get_or_create_notifications(
            hass,
        ).get("aquanode_pulse_ap_429385_connection")
        assert notification is not None
        assert notification["title"] == "Power is back"

        status.return_value = {
            **STATUS,
            "uptime_s": 3,
            "boot_count": 9,
            "voltage": {
                **STATUS["voltage"],
                "voltage_v": 190.0,
            },
        }
        await coordinator.async_refresh()
        await hass.async_block_till_done()

        voltage_incident = entry.runtime_data.history.open_voltage_incident(
            "AP-429385",
        )
        assert voltage_incident is not None
        assert voltage_incident["minimum_voltage"] == 190.0
        voltage_notification = (
            persistent_notification._async_get_or_create_notifications(
                hass,
            ).get("aquanode_pulse_ap_429385_voltage")
        )
        assert voltage_notification is not None
        assert voltage_notification["title"] == "Low voltage"

        status.return_value = {
            **STATUS,
            "uptime_s": 4,
            "boot_count": 9,
            "voltage": {
                **STATUS["voltage"],
                "voltage_v": 204.0,
            },
        }
        await coordinator.async_refresh()
        await hass.async_block_till_done()

        assert entry.runtime_data.history.open_voltage_incident("AP-429385") is None
        voltage_notification = (
            persistent_notification._async_get_or_create_notifications(
                hass,
            ).get("aquanode_pulse_ap_429385_voltage")
        )
        assert voltage_notification is not None
        assert voltage_notification["title"] == "Voltage recovered"
        saved = entry.runtime_data.history.payload("AP-429385", "day")
        assert saved["saved_event_count"] == 2
        assert saved["voltage"]
        assert saved["voltage"][-1]["minimum"] == 190.0

    assert await hass.config_entries.async_unload(entry.entry_id)


@pytest.mark.asyncio
async def test_response_stall_is_filtered_but_a_reboot_is_kept(
    hass: HomeAssistant,
    mock_async_zeroconf,
) -> None:
    """Ignore a busy HTTP loop, while retaining short power-cut evidence."""
    assert mock_async_zeroconf is not None
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: "192.0.2.42",
            CONF_PORT: 6053,
            CONF_PASSWORD: "test-password",
        },
        title="Acasă",
        unique_id="AP-429385",
    )
    entry.add_to_hass(hass)

    status = AsyncMock(return_value=STATUS)
    with patch(
        "custom_components.aquanode_pulse.api.AquaNodePulseApi.async_status",
        status,
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        coordinator = entry.runtime_data.coordinator

        diagnostic_switch = _metrics(hass)["diagnostic_logging"]
        assert diagnostic_switch.state == STATE_OFF
        await hass.services.async_call(
            "switch",
            "turn_on",
            {"entity_id": diagnostic_switch.entity_id},
            blocking=True,
        )
        assert coordinator.diagnostic_logging_enabled
        assert _metrics(hass)["diagnostic_logging"].state == STATE_ON

        status.side_effect = AquaNodePulseResponseTimeout()
        await coordinator.async_refresh()
        await hass.async_block_till_done()

        local_connection = _metrics(hass)["local_connection"]
        assert local_connection.state == STATE_ON
        assert local_connection.attributes["poll_issue_count"] == 1
        assert local_connection.attributes["filtered_poll_gaps"] == 0
        assert entry.runtime_data.history.pending_connection("AP-429385") is None
        assert entry.runtime_data.history.last_interruption("AP-429385") is None

        status.side_effect = None
        status.return_value = STATUS
        await coordinator.async_refresh()
        await hass.async_block_till_done()

        local_connection = _metrics(hass)["local_connection"]
        assert local_connection.state == STATE_ON
        assert local_connection.attributes["filtered_poll_gaps"] == 1
        assert local_connection.attributes["consecutive_poll_issues"] == 0
        assert entry.runtime_data.history.last_interruption("AP-429385") is None

        status.side_effect = AquaNodePulseResponseTimeout()
        await coordinator.async_refresh()
        await hass.async_block_till_done()
        status.side_effect = None
        status.return_value = {
            **STATUS,
            "uptime_s": 2,
            "boot_count": 9,
        }
        await coordinator.async_refresh()
        await hass.async_block_till_done()

        interruption = entry.runtime_data.history.last_interruption("AP-429385")
        assert interruption is not None
        assert interruption["kind"] == "power"
        assert _metrics(hass)["local_connection"].state == STATE_ON

    assert await hass.config_entries.async_unload(entry.entry_id)


@pytest.mark.asyncio
async def test_wifi_evidence_filters_poll_gaps_and_ups_mode_is_opt_in(
    hass: HomeAssistant,
    mock_async_zeroconf,
) -> None:
    """Keep real Wi-Fi reconnects, remove poll gaps and opt in to UPS alerts."""
    assert mock_async_zeroconf is not None
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: "192.0.2.42",
            CONF_PORT: 6053,
            CONF_PASSWORD: "test-password",
        },
        title="Acasă",
        unique_id="AP-429385",
    )
    entry.add_to_hass(hass)

    status = AsyncMock(return_value=STATUS)
    with patch(
        "custom_components.aquanode_pulse.api.AquaNodePulseApi.async_status",
        status,
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        coordinator = entry.runtime_data.coordinator

        assert _metrics(hass)["router_on_ups"].state == STATE_OFF

        # A single failed TCP connection followed by the same firmware counters
        # is not a network event and never turns the entity off.
        status.side_effect = AquaNodePulseCannotConnect()
        await coordinator.async_refresh()
        await hass.async_block_till_done()
        assert _metrics(hass)["local_connection"].state == STATE_ON

        status.side_effect = None
        status.return_value = STATUS
        await coordinator.async_refresh()
        await hass.async_block_till_done()
        assert entry.runtime_data.history.last_interruption("AP-429385") is None
        assert _metrics(hass)["local_connection"].attributes["filtered_poll_gaps"] == 1

        # The same boot plus a moved firmware Wi-Fi counter is a real network
        # interruption even if only one local poll failed.
        status.side_effect = AquaNodePulseCannotConnect()
        await coordinator.async_refresh()
        await hass.async_block_till_done()
        status.side_effect = None
        status.return_value = {
            **STATUS,
            "uptime_s": 12_347,
            "wifi": {
                **STATUS["wifi"],
                "disconnect_count": 1,
            },
        }
        await coordinator.async_refresh()
        await hass.async_block_till_done()
        interruption = entry.runtime_data.history.last_interruption("AP-429385")
        assert interruption is not None
        assert interruption["kind"] == "network"
        assert interruption["evidence"] == "wifi_disconnect_count"

        # UPS mode is explicitly off by default. Once enabled, one strong
        # unreachable result is enough to issue the assumed-power warning.
        router_switch = _metrics(hass)["router_on_ups"]
        await hass.services.async_call(
            "switch",
            "turn_on",
            {"entity_id": router_switch.entity_id},
            blocking=True,
        )
        assert coordinator.router_on_ups_enabled
        assert _metrics(hass)["router_on_ups"].state == STATE_ON

        status.side_effect = AquaNodePulseCannotConnect()
        await coordinator.async_refresh()
        await hass.async_block_till_done()
        assert _metrics(hass)["local_connection"].state == STATE_OFF
        notification = persistent_notification._async_get_or_create_notifications(
            hass,
        ).get("aquanode_pulse_ap_429385_connection")
        assert notification is not None
        assert notification["title"] == "Power outage detected"

        # No reboot and no Wi-Fi counter movement proves this was merely a
        # local poll gap. It is removed from history and the warning corrected.
        status.side_effect = None
        await coordinator.async_refresh()
        await hass.async_block_till_done()
        corrected = persistent_notification._async_get_or_create_notifications(
            hass,
        ).get("aquanode_pulse_ap_429385_connection")
        assert corrected is not None
        assert corrected["title"] == "Alert corrected"
        assert entry.runtime_data.history.last_interruption("AP-429385") == interruption

    assert await hass.config_entries.async_unload(entry.entry_id)


class _FailingRequest:
    def __init__(self, error: Exception) -> None:
        self._error = error

    async def __aenter__(self):
        raise self._error

    async def __aexit__(self, *args) -> None:
        return None


class _FailingSession:
    def __init__(self, error: Exception) -> None:
        self._error = error

    def request(self, *args, **kwargs):
        return _FailingRequest(self._error)


class _BodyTimeoutResponse:
    status = 200

    async def json(self, **kwargs):
        raise SocketTimeoutError


class _ReturningRequest:
    async def __aenter__(self):
        return _BodyTimeoutResponse()

    async def __aexit__(self, *args) -> None:
        return None


class _BodyTimeoutSession:
    def request(self, *args, **kwargs):
        return _ReturningRequest()


@pytest.mark.asyncio
async def test_api_distinguishes_response_and_connection_timeouts() -> None:
    """Preserve the signal the coordinator needs for correct classification."""
    response_api = AquaNodePulseApi(
        _FailingSession(SocketTimeoutError()),
        "192.0.2.42",
        6053,
        "test-password",
    )
    with pytest.raises(AquaNodePulseResponseTimeout):
        await response_api.async_status()

    body_timeout_api = AquaNodePulseApi(
        _BodyTimeoutSession(),
        "192.0.2.42",
        6053,
        "test-password",
    )
    with pytest.raises(AquaNodePulseResponseTimeout):
        await body_timeout_api.async_status()

    connection_api = AquaNodePulseApi(
        _FailingSession(ConnectionTimeoutError()),
        "192.0.2.42",
        6053,
        "test-password",
    )
    with pytest.raises(AquaNodePulseCannotConnect):
        await connection_api.async_status()


@pytest.mark.asyncio
async def test_old_two_second_network_artifacts_are_migrated(
    hass: HomeAssistant,
) -> None:
    """Remove only legacy short network rows that had no firmware evidence."""
    history = PulseHistory(hass)
    await history.async_load()
    current = time.time()
    history.data["devices"]["AP-429385"] = {
        "history_format": 1,
        "events": [
            {
                "id": "legacy-short",
                "kind": "network",
                "started_at": current - 32,
                "ended_at": current - 30,
                "duration_seconds": 2.0,
            },
            {
                "id": "real-wifi",
                "kind": "network",
                "started_at": current - 22,
                "ended_at": current - 20,
                "duration_seconds": 2.0,
                "evidence": "wifi_disconnect_count",
            },
            {
                "id": "legacy-long",
                "kind": "network",
                "started_at": current - 16,
                "ended_at": current - 10,
                "duration_seconds": 6.0,
            },
        ],
        "voltage": {},
        "last_boot_count": 8,
        "last_wifi_disconnect_count": 0,
        "last_voltage": None,
        "pending_connection": None,
    }
    await history.async_save()

    reloaded = PulseHistory(hass)
    await reloaded.async_load()
    ids = {
        event["id"] for event in reloaded.payload("AP-429385", "year")["recent_events"]
    }
    assert ids == {"real-wifi", "legacy-long"}
