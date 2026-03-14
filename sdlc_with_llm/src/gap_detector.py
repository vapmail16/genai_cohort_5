"""Compliance gap detection service."""

from dataclasses import dataclass

from .models import ComplianceGap
from .data_loader import load_regulatory_requirements, load_compliance_info


@dataclass
class GapDetectionResult:
    """Result of compliance gap detection."""

    gaps: list[ComplianceGap]
    success: bool
    limited_due_to_missing_docs: bool
    message: str


def detect_compliance_gaps(
    compliance_file: str = "compliance_info.json",
    requirements_file: str = "regulatory_requirements.json",
) -> GapDetectionResult:
    """
    Analyze regulatory requirements vs compliance documentation to find gaps.

    Args:
        compliance_file: JSON file with compliance documents.

    Returns:
        GapDetectionResult with identified gaps and metadata.
    """
    requirements = load_regulatory_requirements(requirements_file)
    compliance_docs, missing_req_ids = load_compliance_info(compliance_file)

    doc_by_req = {d.requirement_id: d for d in compliance_docs}
    req_by_id = {r.id: r for r in requirements}

    gaps = []
    limited = False

    if not requirements:
        return GapDetectionResult(
            gaps=[],
            success=True,
            limited_due_to_missing_docs=False,
            message="No regulatory requirements available for comparison.",
        )

    if not compliance_docs and not missing_req_ids:
        limited = True
        for req in requirements:
            gaps.append(
                ComplianceGap(
                    requirement_id=req.id,
                    regulation_id=req.regulation_id,
                    regulation_name=req.regulation_name,
                    requirement_text=req.requirement_text,
                    gap_reason="No compliance documentation available for comparison.",
                    severity="high",
                )
            )
        return GapDetectionResult(
            gaps=gaps,
            success=True,
            limited_due_to_missing_docs=True,
            message="Complete gap analysis may be limited due to missing documentation.",
        )

    for req in requirements:
        if req.id in missing_req_ids:
            gaps.append(
                ComplianceGap(
                    requirement_id=req.id,
                    regulation_id=req.regulation_id,
                    regulation_name=req.regulation_name,
                    requirement_text=req.requirement_text,
                    gap_reason="No compliance documentation found for this requirement.",
                    severity="high",
                )
            )
        elif req.id in doc_by_req:
            doc = doc_by_req[req.id]
            if doc.status != "compliant":
                gaps.append(
                    ComplianceGap(
                        requirement_id=req.id,
                        regulation_id=req.regulation_id,
                        regulation_name=req.regulation_name,
                        requirement_text=req.requirement_text,
                        gap_reason=f"Documentation status: {doc.status}. {doc.evidence}",
                        severity="high" if doc.status == "non_compliant" else "medium",
                    )
                )

    if missing_req_ids and len(compliance_docs) < len(requirements):
        limited = True

    message = ""
    if limited:
        message = "Complete gap analysis may be limited due to missing documentation."
    elif not gaps:
        message = "No compliance gaps were found."

    return GapDetectionResult(
        gaps=gaps,
        success=True,
        limited_due_to_missing_docs=limited,
        message=message,
    )
