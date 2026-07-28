"""End-to-end setup and interruption checks against real Home Assistant."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.components import persistent_notification
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import CONF_HOST, STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.aquanode_pulse.api import AquaNodePulseCannotConnect
from custom_components.aquanode_pulse.const import (
    CONF_PASSWORD,
    CONF_PORT,
    DOMAIN,
)

pytestmark = pytest.mark.usefixtures("enable_custom_integrations")

STATUS = {
    "api_version": 1,
    "serial": "AP-429385",
    "name": "AquaNode Pulse 429385",
    "model": "AquaNode Pulse",
    "firmware": "1.3.0",
    "uptime_s": 12_345,
    "boot_count": 8,
    "wifi": {
        "connected": True,
        "rssi_dbm": -58,
        "ip": "192.0.2.42",
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
            "display_name",
            "last_interruption_started",
            "last_voltage",
            "local_connection",
            "notification_delay",
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
