---
title: LIFTED ANALYTICS DASHBOARD
colorFrom: yellow
colorTo: indigo
sdk: docker
app_port: 8501
pinned: false
---

# LiftED Analytics Dashboard

Streamlit programme dashboard. Tech Team, Peepul.

## Excel source

The app reads an uploaded management workbook, or the local `LiftED Cohort 2_Program Management Hub.xlsx` when present. Otherwise, hosting uses `workbook_snapshot.json`, an extract generated from that workbook. Uploads replace data for the current session only. They are not published or saved.

To update the published extract:

```powershell
python workbook_data.py "path/to/LiftED Cohort 2_Program Management Hub.xlsx"
python generate_zone_briefs.py
python -m unittest test_workbook_data.py
```

Review changed figures and Qwen recommendations before publishing the JSON files. The tests include reconciliation values for the original workbook and must be reviewed when the reporting source changes. Extracts omit principal names, phone numbers and personal staff notes. The original workbook is excluded from Git and Docker.

## Metric sources

| Section | Workbook source | Treatment |
|---|---|---|
| Reach and schools | School Allocation; Leadership Update 9 Sep | Unique IDs, zone counts, attendance numerator/denominator, completed/planned batches |
| Learning | Competency Based Inputs (wip) | Recorded programme-level performance and targets; no invented zone splits |
| Teacher practice | TP adoption KPI and targets | Targets only; actuals unavailable |
| Field operations | Leadership Update 9 Sep; Manager's Check-in | Separate recorded periods; no blank-to-zero conversion or inferred zone assignments |
| Risks | Accountability & Risk | Original dated risks; no inferred current status |
| Evaluation | Result Framework OY4 | Baseline/target/result columns preserved; no inferred causal impact |
| School brief | School Allocation | Allocation facts only; diagnoses unavailable |

Every displayed record carries a source sheet and row reference. Qwen uses only verified zone allocation and training evidence. It does not produce unsupported learning scores. Source hashes prevent old briefs being shown for changed workbooks. No automatic weekly refresh is configured.
