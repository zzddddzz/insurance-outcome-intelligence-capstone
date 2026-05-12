# P2 Feedback Cleanup Decisions

Created on `2026-05-12`

## Classification Rules

- `Phase 1`: direct main-report edits that can be completed in the live Google Doc with existing evidence.
- `Phase 2`: evidence-backed additions that require repo output, screenshot verification, or model execution before the report should claim them.
- `Phase 3`: final deliverables, exports, or separate document creation after main report cleanup.
- `Exception`: intentionally unresolved or keep-as-is item with an explicit reason.

## Current Decisions

- 2026-05-12: Treat the live Google Doc as the source of truth for report text, comments, table numbering, and resolved/unresolved feedback state. Repo files are supporting evidence.
- 2026-05-12: Track the current work in this repository because the remaining feedback references repo assets (`dashboard.py`, `streamlit_app.py`, `output/`, `src/`, and model outputs), even though the report itself is in Google Docs.
- 2026-05-12: EDA interpretation is the next recommended item because it is mostly prose and can be verified directly in the Google Doc before screenshot/model work.
- 2026-05-12: The model-comparison comment stays Phase 2 because it should not be resolved until benchmark metrics are actually run or located from authoritative repo output.
- 2026-05-12: The separate Executive Summary comment stays Phase 3 because a stronger main-report executive section does not satisfy a request for a separate CEO-ready document.

## Source-Of-Truth Rules

- For Google Doc prose/comments: use `P2 Initial Findings Report - Team 54 v2`, document ID `1qROBjYtdrFew8WJbOoN8efbboXYSREfCGxY6kXNmxnU`.
- For model metrics: use repo code/output, especially `src/models.py`, `src/train_pipeline.py`, `output/model_summary.json`, `output/feature_importance.csv`, and `output/claim_feature_importance.csv`.
- For dashboard screenshots: use live dashboard rendering or verified files under `output/dashboard_screenshots_euro/`; do not assume a screenshot is full-portfolio without checking.
- For Canvas instructions/comments: use the live Canvas/Google Doc state if anything appears inconsistent.

## Writing Rules

- Keep additions student-report-like: concise, evidence-backed, and not overly polished.
- Avoid filler phrases that sound generic; each added paragraph should connect to a table, figure, model result, output file, or decision implication.
- Use normal paragraph spacing in the Google Doc; do not add manual blank paragraphs unless the surrounding section already uses them deliberately.

## Sensitive Information Rule

- Do not store live passwords, PINs, access tokens, recovery codes, PHI, or other secrets in project docs.
- Refer to source paths, doc IDs, or redacted values instead.

## Update Rule

If a file/task changes bucket, add a new dated note with:

- old bucket
- new bucket
- why the classification changed
