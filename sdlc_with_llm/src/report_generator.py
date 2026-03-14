"""Compliance report generation service."""

from datetime import datetime, timezone

from .models import ComplianceReport
from .data_loader import (
    load_regulatory_requirements,
    load_compliance_info,
)


def generate_compliance_report(
    compliance_file: str = "compliance_info.json",
    requirements_file: str = "regulatory_requirements.json",
) -> ComplianceReport:
    """
    Generate a structured compliance report from available data.

    Args:
        compliance_file: JSON file with compliance documents.

    Returns:
        ComplianceReport or indication that generation cannot be completed.
    """
    requirements = load_regulatory_requirements(requirements_file)
    compliance_docs, missing_req_ids = load_compliance_info(compliance_file)

    # Check if we have any data to work with
    if not requirements and not compliance_docs:
        return ComplianceReport(
            id="report-none",
            generated_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            applicable_regulations=[],
            compliance_status={},
            summary="Report generation cannot be completed: no compliance "
            "information and no applicable regulatory requirements available.",
            can_generate=False,
        )

    # Build regulation -> status mapping from compliance docs
    req_by_id = {r.id: r for r in requirements}
    doc_by_req = {d.requirement_id: d for d in compliance_docs}

    applicable_regulations = list(
        {r.regulation_name for r in requirements}
        | {d.regulation_id for d in compliance_docs}
    )

    compliance_status = {}
    for req in requirements:
        if req.id in doc_by_req:
            doc = doc_by_req[req.id]
            compliance_status[req.requirement_text] = doc.status
        elif req.id in missing_req_ids:
            compliance_status[req.requirement_text] = "missing"
        else:
            compliance_status[req.requirement_text] = "unknown"

    for doc in compliance_docs:
        if doc.requirement_id not in req_by_id:
            compliance_status[f"[{doc.document_name}]"] = doc.status

    summary_parts = []
    summary_parts.append(
        f"Applicable regulations: {', '.join(applicable_regulations)}."
    )
    compliant = sum(1 for s in compliance_status.values() if s == "compliant")
    partial = sum(1 for s in compliance_status.values() if s == "partial")
    missing = sum(1 for s in compliance_status.values() if s == "missing")
    summary_parts.append(
        f"Current compliance status: {compliant} compliant, "
        f"{partial} partial, {missing} missing documentation."
    )
    if missing or partial:
        summary_parts.append(
            "Missing information is not falsely presented as complete."
        )

    now = datetime.now(timezone.utc)
    return ComplianceReport(
        id=f"report-{now.strftime('%Y%m%d%H%M%S')}",
        generated_at=now.isoformat().replace("+00:00", "Z"),
        applicable_regulations=applicable_regulations,
        compliance_status=compliance_status,
        summary=" ".join(summary_parts),
        can_generate=True,
    )
