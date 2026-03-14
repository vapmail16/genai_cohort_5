"""Data models for Compliance & Audit Copilot."""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class RegulatorySource:
    """A configured regulatory source to monitor."""

    id: str
    name: str
    source_type: str
    url: str
    enabled: bool
    last_checked: Optional[str] = None
    available: bool = True


@dataclass
class RegulatoryUpdate:
    """A new or modified regulatory requirement."""

    id: str
    source_id: str
    regulation_id: str
    regulation_name: str
    title: str
    summary: str
    effective_date: str
    status: str  # "new" or "modified"
    retrieved_at: str


@dataclass
class RegulatoryRequirement:
    """A specific regulatory requirement."""

    id: str
    regulation_id: str
    regulation_name: str
    requirement_text: str
    category: str
    effective_date: str


@dataclass
class ComplianceDocument:
    """Organization's compliance documentation for a requirement."""

    id: str
    requirement_id: str
    regulation_id: str
    document_name: str
    status: str  # "compliant", "partial", "non_compliant"
    last_reviewed: str
    evidence: str


@dataclass
class ComplianceGap:
    """Identified gap between regulatory requirement and compliance documentation."""

    requirement_id: str
    regulation_id: str
    regulation_name: str
    requirement_text: str
    gap_reason: str
    severity: str = "medium"


@dataclass
class MonitoringResult:
    """Result of regulatory monitoring process."""

    success: bool
    updates: list[RegulatoryUpdate] = field(default_factory=list)
    unavailable_sources: list[str] = field(default_factory=list)
    message: str = ""


@dataclass
class ComplianceReport:
    """Generated compliance report."""

    id: str
    generated_at: str
    applicable_regulations: list[str]
    compliance_status: dict[str, str]
    summary: str
    can_generate: bool = True
