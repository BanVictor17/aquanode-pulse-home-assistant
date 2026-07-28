#!/usr/bin/env python3
"""Fast repository checks that do not require a Home Assistant installation."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "aquanode_pulse"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as err:
        fail(f"{path.relative_to(ROOT)}: {err}")


for path in sorted(COMPONENT.rglob("*.py")):
    try:
        ast.parse(path.read_text(), filename=str(path))
    except (OSError, SyntaxError) as err:
        fail(f"{path.relative_to(ROOT)}: {err}")


def check_imports() -> str:
    """Import every module for real, when Home Assistant is available.

    Parsing only proves the syntax is valid. It cannot see that a name has moved
    to another Home Assistant module, which is how `ConfigFlowResult` shipped
    imported from `data_entry_flow`: the file parsed, the import raised, the
    flow never registered, and the only symptom was "Invalid handler specified"
    in the browser.
    """
    try:
        import homeassistant
    except ImportError:
        return "SKIP: import check needs `pip install homeassistant`"

    import importlib

    sys.path.insert(0, str(ROOT))
    for module in sorted(path.stem for path in COMPONENT.glob("*.py")):
        name = f"custom_components.aquanode_pulse.{module}"
        try:
            importlib.import_module(name)
        except Exception as err:  # noqa: BLE001 - any failure is a failure
            fail(f"{name}: {type(err).__name__}: {err}")

    # Importing is not the same as registering. Subclassing ConfigFlow with
    # `domain=` is what puts the handler in HANDLERS, and an empty HANDLERS is
    # precisely what Home Assistant reports as "Invalid handler specified".
    from homeassistant.config_entries import HANDLERS

    if HANDLERS.get("aquanode_pulse") is None:
        fail("config flow did not register: Home Assistant would refuse to add it")

    # The mDNS record the board really advertises, straight from `dns-sd -L`.
    # Raw ServiceInfo properties are keyed by bytes, so reading them with a str
    # key returns nothing and every board is silently rejected as "not ours".
    import socket

    from zeroconf import ServiceInfo

    from custom_components.aquanode_pulse.config_flow import _extract

    info = ServiceInfo(
        "_aquanode-pulse._tcp.local.",
        "AquaNode Pulse 429385._aquanode-pulse._tcp.local.",
        addresses=[socket.inet_aton("192.168.1.42")],
        port=6053,
        properties={"serial": "AP-429385", "model": "pulse", "api": "1"},
        server="aquanode-pulse-429385.local.",
    )
    if _extract(info) != ("AP-429385", "192.168.1.42", 6053):
        fail(f"discovery would not recognise a real board: {_extract(info)}")

    stranger = ServiceInfo(
        "_aquanode-pulse._tcp.local.",
        "somebody else._aquanode-pulse._tcp.local.",
        addresses=[socket.inet_aton("192.168.1.43")],
        port=6053,
        properties={"model": "pulse"},
        server="stranger.local.",
    )
    if _extract(stranger) is not None:
        fail("discovery accepted a service with no serial")

    # Importing the module never executes the scan, which is how a browser
    # built without a handler shipped and turned every attempt to add the
    # integration into a 500. So run the whole function, with a throwaway
    # zeroconf standing in for the one Home Assistant would hand it.
    import asyncio

    from zeroconf.asyncio import AsyncZeroconf

    from custom_components.aquanode_pulse import config_flow

    async def run_scan() -> None:
        aiozc = AsyncZeroconf()

        async def _fake_instance(hass: object) -> AsyncZeroconf:
            return aiozc

        module = sys.modules["homeassistant.components.zeroconf"]
        real = module.async_get_async_instance
        module.async_get_async_instance = _fake_instance
        original_seconds = config_flow.DISCOVERY_SECONDS
        config_flow.DISCOVERY_SECONDS = 0.1
        try:
            await config_flow._async_scan(None)
        finally:
            config_flow.DISCOVERY_SECONDS = original_seconds
            module.async_get_async_instance = real
            await aiozc.async_close()

    import homeassistant.components.zeroconf  # noqa: F401

    try:
        asyncio.run(run_scan())
    except Exception as err:  # noqa: BLE001 - any failure is a failure
        fail(f"the network scan raises: {type(err).__name__}: {err}")

    # The unicast fallback is the only path that works on a containerised
    # Home Assistant, so it gets a real board to find: an aiohttp app serving
    # exactly what the firmware's handleInfo() returns.
    from aiohttp import ClientSession, web

    async def run_sweep() -> None:
        app = web.Application()
        app.router.add_get(
            "/api/v1/info",
            lambda request: web.json_response(
                {"api_version": 1, "serial": "AP-429385", "name": "Casa"},
            ),
        )
        app.router.add_get(
            "/{tail:.*}", lambda request: web.json_response({"not": "a pulse"})
        )
        runner = web.AppRunner(app)
        await runner.setup()
        await web.TCPSite(runner, "127.0.0.1", 6053).start()

        session = ClientSession()
        real_session = config_flow.async_get_clientsession
        config_flow.async_get_clientsession = lambda hass: session
        try:
            found = await config_flow._async_sweep(None, "127.0.0.0/24")
        finally:
            config_flow.async_get_clientsession = real_session
            await session.close()
            await runner.cleanup()

        if found.get("AP-429385", {}).get(CONF_HOST) != "127.0.0.1":
            fail(f"the unicast sweep does not find a board: {found}")

    from homeassistant.const import CONF_HOST

    try:
        asyncio.run(run_sweep())
    except OSError as err:
        print(f"SKIP: sweep check needs port 6053 free ({err})")
    except Exception as err:  # noqa: BLE001 - any failure is a failure
        fail(f"the unicast sweep raises: {type(err).__name__}: {err}")

    # The classification is the whole point of the product, so it gets the
    # scenarios rather than a smoke test.
    from custom_components.aquanode_pulse.interruptions import (
        NETWORK,
        POWER,
        UNKNOWN,
        InterruptionTracker,
        classify,
    )

    cases = [
        # a restart moved the boot counter: the mains went away
        ((7, 8, 12.0, 300.0), POWER),
        # same counter, so the board was powered the whole time
        ((7, 7, 4000.0, 300.0), NETWORK),
        # no counter, but it has been up longer than it was missing
        ((None, None, 4000.0, 300.0), NETWORK),
        # no counter and no proof either way: say so
        ((None, None, 10.0, 300.0), UNKNOWN),
    ]
    for args, expected in cases:
        if (actual := classify(*args)) != expected:
            fail(f"classify{args} said {actual}, expected {expected}")

    tracker = InterruptionTracker()
    tracker.poll_succeeded(0.0, {"boot_count": 7, "uptime_s": 900})
    tracker.poll_failed(100.0)
    tracker.poll_failed(160.0)  # still away; the start must not move
    event = tracker.poll_succeeded(400.0, {"boot_count": 8, "uptime_s": 20})
    if event is None or event.cause != POWER or event.duration_seconds != 300.0:
        fail(f"the tracker misread a power cut: {event}")

    short = InterruptionTracker()
    short.poll_succeeded(0.0, {"boot_count": 7, "uptime_s": 900})
    short.poll_failed(10.0, 1_000.0)
    short_event = short.poll_succeeded(
        12.0,
        {"boot_count": 7, "uptime_s": 912},
        1_002.0,
    )
    if (
        short_event is None
        or short_event.cause != NETWORK
        or short_event.duration_seconds != 2.0
        or short_event.started_at != 1_000.0
    ):
        fail(f"a two second interruption was not retained: {short_event}")

    restored = InterruptionTracker()
    restored.restore_boot_count(41)
    restored.poll_failed(10.0, 1_000.0)
    restored_event = restored.poll_succeeded(
        15.0,
        {"boot_count": 42, "uptime_s": 3},
        1_005.0,
    )
    if restored_event is None or restored_event.cause != POWER:
        fail(f"persisted boot evidence was ignored: {restored_event}")

    resumed = InterruptionTracker()
    resumed.restore_boot_count(41)
    resumed.restore_offline(100.0, 1_005.0, 1_000.0)
    resumed_event = resumed.poll_succeeded(
        102.0,
        {"boot_count": 42, "uptime_s": 3},
        1_007.0,
    )
    if (
        resumed_event is None
        or resumed_event.cause != POWER
        or resumed_event.started_at != 1_000.0
        or resumed_event.duration_seconds != 7.0
    ):
        fail(f"an interruption spanning an HA restart was lost: {resumed_event}")

    from custom_components.aquanode_pulse.history import add_to_bucket, prune_rows

    rows = []
    if not add_to_bucket(rows, 60, 230.0, 60):
        fail("the first voltage sample did not open a bucket")
    if add_to_bucket(rows, 61, 232.0, 60):
        fail("a sample in the same minute opened another bucket")
    if rows != [
        {
            "at": 60,
            "minimum": 230.0,
            "maximum": 232.0,
            "average": 231.0,
            "count": 2,
        }
    ]:
        fail(f"voltage aggregation is wrong: {rows}")
    add_to_bucket(rows, 120, 228.0, 60)
    prune_rows(rows, 100)
    if len(rows) != 1 or rows[0]["at"] != 120:
        fail(f"voltage retention is wrong: {rows}")

    # Prove that graphs and events actually survive a Home Assistant restart,
    # rather than only checking the in-memory aggregation helpers.
    import tempfile
    import time

    from homeassistant.core import HomeAssistant

    from custom_components.aquanode_pulse.history import PulseHistory

    async def run_persistence() -> None:
        with tempfile.TemporaryDirectory() as config_dir:
            hass = HomeAssistant(config_dir)
            now = time.time()
            history = PulseHistory(hass)
            await history.async_load()
            history.record_voltage("AP-429385", now, 231.4)
            await history.async_start_connection_loss(
                "AP-429385",
                started_at=now - 2,
                maintenance_until=None,
            )
            await history.async_save()

            restored = PulseHistory(hass)
            await restored.async_load()
            pending = restored.pending_connection("AP-429385")
            if pending is None or pending["started_at"] != round(now - 2, 3):
                fail(f"active connection loss was not restored: {pending}")
            await restored.async_add_interruption(
                "AP-429385",
                cause=POWER,
                started_at=float(pending["started_at"]),
                ended_at=now,
                duration_seconds=2,
            )

            reloaded = PulseHistory(hass)
            await reloaded.async_load()
            if reloaded.pending_connection("AP-429385") is not None:
                fail("completed connection loss remained marked as active")
            payload = reloaded.payload("AP-429385", "year")
            if (
                payload["saved_event_count"] != 1
                or payload["power_outage_count"] != 1
                or payload["last_voltage"]["value"] != 231.4
                or len(payload["voltage"]) != 1
            ):
                fail(f"persistent history did not round-trip: {payload}")
            await hass.async_stop(force=True)

    try:
        asyncio.run(run_persistence())
    except Exception as err:  # noqa: BLE001 - persistence must really work
        fail(f"persistent history raises: {type(err).__name__}: {err}")

    # Parse the phone automation through Home Assistant's real blueprint
    # schema. Plain YAML parsing would miss invalid selectors and inputs.
    from homeassistant.components.automation.config import (
        AUTOMATION_BLUEPRINT_SCHEMA,
    )
    from homeassistant.components.blueprint.models import Blueprint
    from homeassistant.util.yaml import load_yaml

    blueprint_path = (
        ROOT
        / "blueprints"
        / "automation"
        / "aquanode_pulse"
        / "interruption_alert.yaml"
    )
    try:
        Blueprint(
            load_yaml(blueprint_path),
            path=str(blueprint_path),
            expected_domain="automation",
            schema=AUTOMATION_BLUEPRINT_SCHEMA,
        )
    except Exception as err:  # noqa: BLE001 - schema rejection is a failure
        fail(f"phone blueprint is invalid: {type(err).__name__}: {err}")

    return (
        "ok: imports, flow, mDNS, scan, sweep, interruption classification "
        "and persistent voltage/event history"
    )


import_result = check_imports()

manifest = load_json(COMPONENT / "manifest.json")
hacs = load_json(ROOT / "hacs.json")
strings = load_json(COMPONENT / "strings.json")
english = load_json(COMPONENT / "translations" / "en.json")
romanian = load_json(COMPONENT / "translations" / "ro.json")

required_manifest = {
    "domain",
    "name",
    "version",
    "codeowners",
    "config_flow",
    "documentation",
    "issue_tracker",
    "integration_type",
    "iot_class",
    "zeroconf",
}
missing = required_manifest - manifest.keys()
if missing:
    fail(f"manifest keys missing: {sorted(missing)}")
manifest_keys = list(manifest)
expected_manifest_keys = [
    "domain",
    "name",
    *sorted(set(manifest_keys) - {"domain", "name"}),
]
if manifest_keys != expected_manifest_keys:
    fail("manifest keys must be ordered domain, name, then alphabetically")
if manifest.get("dependencies") != sorted(manifest.get("dependencies", [])):
    fail("manifest dependencies must be sorted alphabetically")
if manifest["domain"] != "aquanode_pulse":
    fail("unexpected integration domain")
if "_aquanode-pulse._tcp.local." not in manifest["zeroconf"]:
    fail("mDNS service is not registered in manifest")
if not hacs.get("name"):
    fail("hacs.json has no name")
if strings != english:
    fail("strings.json and English translation differ")
if set(strings["entity"]) != set(romanian["entity"]):
    fail("Romanian entity groups do not match English")
for platform, entities in strings["entity"].items():
    if set(entities) != set(romanian["entity"].get(platform, {})):
        fail(f"Romanian {platform} entities do not match English")
if manifest["version"] != "0.5.0":
    fail("manifest version was not bumped for the dashboard/history release")

frontend = (COMPONENT / "frontend" / "aquanode-pulse-panel.js").read_text()
for contract in (
    "aquanode_pulse/history",
    "aquanode_pulse/clear_history",
    "data-device-tab",
    "voltageChart",
    "outageChart",
    "set-notification-delay",
    "phone-help",
    "rename-device",
    "test-notification",
):
    if contract not in frontend:
        fail(f"frontend contract missing: {contract}")

blueprint = (
    ROOT / "blueprints" / "automation" / "aquanode_pulse" / "interruption_alert.yaml"
).read_text()
for event_type in (
    "aquanode_pulse_interruption",
    "aquanode_pulse_voltage_low",
    "aquanode_pulse_voltage_recovered",
):
    if event_type not in blueprint:
        fail(f"mobile blueprint does not handle {event_type}")

firmware = (
    ROOT.parent
    / "AquaNode Pulse"
    / "Firmware"
    / "AquaNodePulse"
    / "pulse_home_assistant.cpp"
)
if firmware.exists():
    source = firmware.read_text()
    for contract in (
        'MDNS.addService("aquanode-pulse", "tcp"',
        '"/api/v1/status"',
        '"Authorization"',
        '\\"voltage_v\\"',
    ):
        if contract not in source:
            fail(f"firmware contract missing: {contract}")

print(import_result)
print("AquaNode Pulse Home Assistant checks: all passed")
