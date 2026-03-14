"""Regulatory monitoring service - retrieves updates from configured sources."""

from .models import MonitoringResult, RegulatoryUpdate
from .data_loader import load_regulatory_sources, load_regulatory_updates


def monitor_regulations(
    sources_available: dict[str, bool] | None = None,
    updates_file: str = "regulatory_updates.json",
) -> MonitoringResult:
    """
    Monitor configured regulatory sources and retrieve updates.

    Args:
        sources_available: Optional dict mapping source_id -> bool for availability.
            Used to simulate unavailable sources (e.g. {"src-001": False}).
        updates_file: JSON file to load updates from (for testing empty vs populated).

    Returns:
        MonitoringResult with updates, unavailable sources, and status.
    """
    sources = load_regulatory_sources(sources_available)
    enabled_sources = [s for s in sources if s.enabled]

    if not enabled_sources:
        return MonitoringResult(
            success=False,
            updates=[],
            unavailable_sources=[],
            message="No regulatory sources are configured.",
        )

    unavailable = [s.name for s in enabled_sources if not s.available]
    available_sources = [s for s in enabled_sources if s.available]

    # Load updates only from available sources
    all_updates = load_regulatory_updates(updates_file)
    updates = [
        u
        for u in all_updates
        if any(s.id == u.source_id for s in available_sources)
    ]

    return MonitoringResult(
        success=True,
        updates=updates,
        unavailable_sources=unavailable,
        message=(
            "No new or modified regulatory requirements were found."
            if not updates and not unavailable
            else (
                f"Source(s) could not be accessed: {', '.join(unavailable)}."
                if unavailable
                else ""
            )
        ),
    )
