#!/usr/bin/env python3
"""Run the Compliance & Audit Copilot application."""

import sys
from pathlib import Path

# Ensure src is on path when run from project root
sys.path.insert(0, str(Path(__file__).parent))

from src.regulatory_monitor import monitor_regulations
from src.report_generator import generate_compliance_report
from src.gap_detector import detect_compliance_gaps


def main():
    """Run all copilot features and display results."""
    print("=" * 60)
    print("  Compliance & Audit Copilot")
    print("=" * 60)

    # 1. Monitor regulatory updates
    print("\n📋 MONITORING REGULATORY UPDATES")
    print("-" * 40)
    result = monitor_regulations()
    if result.success:
        if result.updates:
            for u in result.updates:
                print(f"  • [{u.status.upper()}] {u.regulation_name}: {u.title}")
                print(f"    Effective: {u.effective_date}")
        else:
            print("  No new or modified regulatory requirements found.")
        if result.unavailable_sources:
            print(f"  ⚠ Unavailable: {', '.join(result.unavailable_sources)}")
    else:
        print(f"  Error: {result.message}")

    # 2. Generate compliance report
    print("\n📄 COMPLIANCE REPORT")
    print("-" * 40)
    report = generate_compliance_report()
    if report.can_generate:
        print(f"  Report ID: {report.id}")
        print(f"  Generated: {report.generated_at}")
        print(f"  Regulations: {', '.join(report.applicable_regulations)}")
        print(f"\n  Summary: {report.summary}")
        print("\n  Status by requirement:")
        for req_text, status in list(report.compliance_status.items())[:5]:
            short = (req_text[:50] + "…") if len(req_text) > 50 else req_text
            print(f"    • {short}: {status}")
        if len(report.compliance_status) > 5:
            print(f"    ... and {len(report.compliance_status) - 5} more")
    else:
        print(f"  {report.summary}")

    # 3. Detect compliance gaps
    print("\n🔍 COMPLIANCE GAP DETECTION")
    print("-" * 40)
    gaps_result = detect_compliance_gaps()
    if gaps_result.gaps:
        for g in gaps_result.gaps:
            print(f"  • [{g.severity}] {g.regulation_name}")
            req_short = (g.requirement_text[:60] + "…") if len(g.requirement_text) > 60 else g.requirement_text
            gap_short = (g.gap_reason[:60] + "…") if len(g.gap_reason) > 60 else g.gap_reason
            print(f"    Requirement: {req_short}")
            print(f"    Gap: {gap_short}")
        if gaps_result.limited_due_to_missing_docs:
            print(f"\n  ⚠ {gaps_result.message}")
    else:
        print(f"  {gaps_result.message}")

    print("\n" + "=" * 60)
    print("  Done.")
    print("=" * 60)


if __name__ == "__main__":
    main()
