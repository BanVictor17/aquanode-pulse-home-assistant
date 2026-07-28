"""Work out what an interruption actually was, from local evidence only.

This integration talks to the board over the LAN, so it never sees the cloud
service's verdict. It does not need to. The board keeps a boot counter in
non-volatile storage and reports its uptime, and those two answer the only
question that matters when it comes back:

* the boot counter moved, so the board restarted, so it lost power
* the boot counter did not move, so the board stayed powered the whole time and
  it was the network between it and Home Assistant that went away

There is deliberately no third guess. When the evidence is missing, the answer
is "unknown" and the user is told that instead of a confident invention.

Pure functions and one small dataclass: no Home Assistant, no clock, no I/O, so
every branch is reachable from a test.
"""

from __future__ import annotations

from dataclasses import dataclass

POWER = "power"
NETWORK = "network"
UNKNOWN = "unknown"
MAINTENANCE = "maintenance"


def classify(
    previous_boot_count: int | None,
    boot_count: int | None,
    uptime_s: float | None,
    offline_seconds: float,
) -> str:
    """Name the cause of an interruption that has just ended."""
    if previous_boot_count is not None and boot_count is not None:
        return POWER if boot_count != previous_boot_count else NETWORK

    # Older firmware, or a board first seen while it was already away. Uptime
    # is the fallback: a board that has been up for longer than it was missing
    # cannot have restarted during it.
    if uptime_s is not None and uptime_s > offline_seconds:
        return NETWORK
    return UNKNOWN


@dataclass
class Interruption:
    """One completed gap in contact with the board."""

    cause: str
    started_at: float
    ended_at: float

    @property
    def duration_seconds(self) -> float:
        return max(0.0, self.ended_at - self.started_at)


class InterruptionTracker:
    """Follow one board across failures and recoveries.

    `poll_failed` and `poll_succeeded` return the interruption that just ended,
    or None. Returning it rather than firing a callback keeps this class free
    of Home Assistant, so the coordinator decides what an event looks like.
    """

    def __init__(self) -> None:
        self.last: Interruption | None = None
        self._offline_since: float | None = None
        self._offline_since_wall: float | None = None
        self._boot_count: int | None = None

    @property
    def offline_since(self) -> float | None:
        """When contact was lost, while it is still lost."""
        return self._offline_since

    @property
    def offline_since_wall(self) -> float | None:
        """Unix time at which contact was first lost."""
        return self._offline_since_wall

    def restore_boot_count(self, value: int | None) -> None:
        """Restore classification evidence saved before an HA restart."""
        self._boot_count = value

    def restore_offline(
        self,
        now: float,
        wall_time: float,
        started_at_wall: float,
    ) -> None:
        """Restore a contact loss that began before Home Assistant restarted."""
        elapsed = max(0.0, wall_time - started_at_wall)
        self._offline_since = now - elapsed
        self._offline_since_wall = started_at_wall

    def offline_seconds(self, now: float) -> float:
        """Return the current contact-loss duration."""
        if self._offline_since is None:
            return 0.0
        return max(0.0, now - self._offline_since)

    def poll_failed(self, now: float, wall_time: float | None = None) -> bool:
        """Record a failed poll and return True only for the first failure."""
        if self._offline_since is None:
            self._offline_since = now
            self._offline_since_wall = wall_time
            return True
        return False

    def poll_succeeded(
        self,
        now: float,
        data: dict,
        wall_time: float | None = None,
    ) -> Interruption | None:
        """The board answered. Returns an interruption if one just ended."""
        boot_count = _integer(data.get("boot_count"))
        uptime = _number(data.get("uptime_s"))
        previous_boot_count = self._boot_count
        self._boot_count = boot_count

        started_at = self._offline_since
        started_at_wall = self._offline_since_wall
        self._offline_since = None
        self._offline_since_wall = None
        if started_at is None:
            return None

        offline_seconds = max(0.0, now - started_at)
        ended_at_wall = wall_time if wall_time is not None else now
        if started_at_wall is None:
            started_at_wall = ended_at_wall - offline_seconds
        self.last = Interruption(
            cause=classify(previous_boot_count, boot_count, uptime, offline_seconds),
            started_at=started_at_wall,
            ended_at=ended_at_wall,
        )
        return self.last


def _integer(value: object) -> int | None:
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def _number(value: object) -> float | None:
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
