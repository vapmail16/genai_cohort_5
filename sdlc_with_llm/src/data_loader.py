"""Load synthetic data from JSON files."""

import json
from pathlib import Path

from .models import (
    RegulatorySource,
    RegulatoryUpdate,
    RegulatoryRequirement,
    ComplianceDocument,
)


DATA_DIR = Path(__file__).parent.parent / "data"


def load_regulatory_sources(
    sources_available: dict[str, bool] | None = None,
) -> list[RegulatorySource]:
    """Load regulatory sources. sources_available overrides availability per source id."""
    path = DATA_DIR / "regulatory_sources.json"
    with open(path) as f:
        data = json.load(f)

    sources = []
    for s in data["sources"]:
        available = s.get("available", True)
        if sources_available is not None and s["id"] in sources_available:
            available = sources_available[s["id"]]
        sources.append(
            RegulatorySource(
                id=s["id"],
                name=s["name"],
                source_type=s["type"],
                url=s["url"],
                enabled=s["enabled"],
                last_checked=s.get("last_checked"),
                available=available,
            )
        )
    return sources


def load_regulatory_updates(
    file_name: str = "regulatory_updates.json",
) -> list[RegulatoryUpdate]:
    """Load regulatory updates from specified file."""
    path = DATA_DIR / file_name
    with open(path) as f:
        data = json.load(f)

    return [
        RegulatoryUpdate(
            id=u["id"],
            source_id=u["source_id"],
            regulation_id=u["regulation_id"],
            regulation_name=u["regulation_name"],
            title=u["title"],
            summary=u["summary"],
            effective_date=u["effective_date"],
            status=u["status"],
            retrieved_at=u["retrieved_at"],
        )
        for u in data.get("updates", [])
    ]


def load_regulatory_requirements(
    file_name: str = "regulatory_requirements.json",
) -> list[RegulatoryRequirement]:
    """Load regulatory requirements from specified file."""
    path = DATA_DIR / file_name
    with open(path) as f:
        data = json.load(f)

    return [
        RegulatoryRequirement(
            id=r["id"],
            regulation_id=r["regulation_id"],
            regulation_name=r["regulation_name"],
            requirement_text=r["requirement_text"],
            category=r["category"],
            effective_date=r["effective_date"],
        )
        for r in data.get("requirements", [])
    ]


def load_compliance_info(
    file_name: str = "compliance_info.json",
) -> tuple[list[ComplianceDocument], list[str]]:
    """Load compliance documents and missing requirement IDs."""
    path = DATA_DIR / file_name
    with open(path) as f:
        data = json.load(f)

    docs = [
        ComplianceDocument(
            id=d["id"],
            requirement_id=d["requirement_id"],
            regulation_id=d["regulation_id"],
            document_name=d["document_name"],
            status=d["status"],
            last_reviewed=d["last_reviewed"],
            evidence=d["evidence"],
        )
        for d in data.get("compliance_documents", [])
    ]
    missing = data.get("missing_requirements", [])
    return docs, missing
