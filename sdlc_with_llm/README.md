# sdlc_with_llm

**Compliance & Audit Copilot** — SDLC with LLM project supporting compliance teams by monitoring regulatory updates, generating compliance reports, and detecting compliance gaps.

Built following the **BRIDGE AI Framework** (Steps 1–7).

## Project Structure

```
sdlc_with_llm/
├── business problem statement   # Business requirements (Step 1)
├── user_stories                 # User stories with acceptance criteria (Step 2)
├── test_cases                   # 15 test cases across 5 user stories (Step 3)
├── data/                        # Synthetic data (Step 4)
│   ├── regulatory_sources.json
│   ├── regulatory_updates.json
│   ├── regulatory_updates_empty.json
│   ├── regulatory_requirements.json
│   ├── regulatory_requirements_empty.json
│   ├── compliance_info.json
│   ├── compliance_info_partial.json
│   ├── compliance_info_empty.json
│   └── compliance_info_full_compliant.json
├── src/                         # Core implementation
│   ├── models.py               # Data models
│   ├── data_loader.py          # JSON data loading
│   ├── regulatory_monitor.py   # Monitor regulatory sources
│   ├── report_generator.py     # Generate compliance reports
│   └── gap_detector.py         # Detect compliance gaps
├── tests/                       # TDD test suite (Step 6 — 38 tests)
│   ├── test_regulatory_monitor.py
│   ├── test_regulatory_review.py
│   ├── test_report_generator.py
│   ├── test_gap_detector.py
│   └── test_audit_preparation.py
├── app.py                       # Flask dashboard (Step 7)
├── templates/                   # Dashboard HTML templates
├── STEP6_EVALUATION.md          # Test evaluation results
└── requirements.txt
```

## Synthetic Data

| File | Purpose |
|------|---------|
| `regulatory_sources.json` | Configured sources (SEC, FINRA, GDPR, etc.) |
| `regulatory_updates.json` | New/modified regulatory updates |
| `regulatory_updates_empty.json` | Empty updates (for "no updates" scenarios) |
| `regulatory_requirements.json` | Regulatory requirements to comply with |
| `compliance_info.json` | Org compliance docs (mix of compliant/partial/missing) |
| `compliance_info_partial.json` | Limited compliance info |
| `compliance_info_empty.json` | No compliance data |
| `compliance_info_full_compliant.json` | Full compliance (no gaps) |

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run the CLI application
python run.py

# Run the web dashboard (Step 7)
python app.py
# Open http://localhost:5000

# Run all tests (Step 6)
pytest tests/ -v
```

```python
from src.regulatory_monitor import monitor_regulations
from src.report_generator import generate_compliance_report
from src.gap_detector import detect_compliance_gaps

# Monitor regulatory updates
result = monitor_regulations()
print(result.updates, result.unavailable_sources)

# Generate compliance report
report = generate_compliance_report()
print(report.summary, report.compliance_status)

# Detect compliance gaps
gaps_result = detect_compliance_gaps()
print(gaps_result.gaps, gaps_result.message)
```

## Test Coverage

All 15 test cases from the requirements are implemented:

- **US1** Monitor Regulatory Updates: 1.1, 1.2, 1.3
- **US2** Review Regulatory Changes: 2.1, 2.2, 2.3
- **US3** Generate Compliance Reports: 3.1, 3.2, 3.3
- **US4** Detect Compliance Gaps: 4.1, 4.2, 4.3
- **US5** Support Audit Preparation: 5.1, 5.2, 5.3

## BRIDGE AI Framework — Steps Completed

| Step | Description | Artifact |
|------|-------------|----------|
| 1 | Business Problem Definition | `business problem statement` |
| 2 | Requirements (User Stories) | `user_stories` |
| 3 | Iterative Testing (Test Cases) | `test_cases` |
| 4 | Data Generation (Synthetic Data) | `data/*.json` |
| 5 | Guided Execution (Code) | `src/*.py` |
| 6 | Evaluate (Test Code) | `STEP6_EVALUATION.md` — 38/38 tests pass |
| 7 | AI-Driven Dashboard | `app.py` + `templates/` |
