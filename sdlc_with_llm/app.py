#!/usr/bin/env python3
"""
Compliance & Audit Copilot — AI-Driven Dashboard (BRIDGE Step 7).

Flask web application presenting regulatory updates, compliance reports,
and compliance gaps with real-time metrics.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask, render_template

from src.regulatory_monitor import monitor_regulations
from src.report_generator import generate_compliance_report
from src.gap_detector import detect_compliance_gaps

app = Flask(__name__)


def _serialize_updates(updates):
    """Convert RegulatoryUpdate objects to dicts for templates."""
    return [
        {
            "id": u.id,
            "regulation_name": u.regulation_name,
            "title": u.title,
            "summary": u.summary,
            "effective_date": u.effective_date,
            "status": u.status,
        }
        for u in updates
    ]


def _serialize_gaps(gaps):
    """Convert ComplianceGap objects to dicts for templates."""
    return [
        {
            "regulation_name": g.regulation_name,
            "requirement_text": g.requirement_text,
            "gap_reason": g.gap_reason,
            "severity": g.severity,
        }
        for g in gaps
    ]


@app.route("/")
def index():
    """Main dashboard with regulatory updates, compliance report, and gaps."""
    # Fetch data from core modules
    monitor_result = monitor_regulations()
    report = generate_compliance_report()
    gaps_result = detect_compliance_gaps()

    # Build metrics for overview
    updates_count = len(monitor_result.updates)
    gaps_count = len(gaps_result.gaps)
    compliant_count = sum(
        1 for s in report.compliance_status.values() if s == "compliant"
    )
    partial_count = sum(
        1 for s in report.compliance_status.values() if s == "partial"
    )
    missing_count = sum(
        1 for s in report.compliance_status.values() if s == "missing"
    )
    total_requirements = len(report.compliance_status)
    compliance_pct = (
        round(100 * compliant_count / total_requirements, 1)
        if total_requirements
        else 0
    )

    return render_template(
        "index.html",
        updates=_serialize_updates(monitor_result.updates),
        unavailable_sources=monitor_result.unavailable_sources,
        report=report,
        gaps=_serialize_gaps(gaps_result.gaps),
        gaps_message=gaps_result.message,
        limited_due_to_missing=gaps_result.limited_due_to_missing_docs,
        # Metrics
        updates_count=updates_count,
        gaps_count=gaps_count,
        compliant_count=compliant_count,
        partial_count=partial_count,
        missing_count=missing_count,
        total_requirements=total_requirements,
        compliance_pct=compliance_pct,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
