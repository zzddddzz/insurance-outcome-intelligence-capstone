# P2 Feedback Cleanup

Project folder: `project/p2-feedback-cleanup`

## How To Use

1. Read this file first.
2. Pick exactly one unchecked item.
3. Do the work in the live Google Doc or repo, whichever is authoritative for that item.
4. Add verification details to `VERIFICATION.md`.
5. Update status here immediately.
6. Record classification/exceptions in `DECISIONS.md`.
7. Update `../INDEX.md` if it exists.

Status key:

- `[ ]` not started
- `[-]` in progress
- `[x]` done
- `[!]` blocked
- `[~]` explicit exception / keep-as-is

## Done-State

- [ ] All instructor-feedback comments in `P2 Initial Findings Report - Team 54 v2` are either resolved or intentionally left open with a reason.
- [ ] The main report clearly shows completed work, remaining work, model evidence, dashboard value, EDA interpretation, and final-deliverable impact.
- [ ] Any dashboard screenshots or model-comparison claims added to the report are verified against the repo outputs or a live run.
- [ ] A separate CEO-ready Executive Summary exists if the team chooses to address that comment now.

## Scope

- In scope: Google Doc feedback cleanup for Part 2 / P2 Initial Findings, report-facing prose, status tables, table numbering, Section 4 synthesis, EDA interpretation notes, dashboard-deliverable framing, model-comparison evidence, and executive-summary planning.
- In scope repo evidence: `dashboard.py`, `streamlit_app.py`, `src/`, `models/`, `output/`, and `README.md`.
- Out of scope: unrelated dashboard product redesign, unrelated Canvas submission mechanics, unrelated report/deck cleanup outside this P2 feedback pass.
- Source of truth: live Google Doc `P2 Initial Findings Report - Team 54 v2`, document ID `1qROBjYtdrFew8WJbOoN8efbboXYSREfCGxY6kXNmxnU`, plus repo outputs under this repository when the report cites model/dashboard evidence.

## Current Focus

- Current phase: `Phase 1: Main report feedback cleanup`
- Next recommended item: `Dashboard deliverable framing: add one clean dashboard screenshot and tie the dashboard to models, segmentation, action queues, and stakeholder decisions.`
- Why this is next: EDA interpretation is now resolved; this is the next unresolved Phase 1 instructor-feedback comment before the heavier model-comparison and screenshot-provenance work.

## Completion Convention

- When every `Done-State` item is `[x]`, do not leave this tracker in a stale active phase.
- Use `Current phase: Maintenance` if the core goal is complete but optional follow-up remains.
- Use `Current phase: Closed` if no active work remains.
- If `Current phase: Closed`, set `Next recommended item` to `none` and add a reopen rule.

## Completed Work Already Landed

- [x] Replaced the Part 2 status writeup under `3. Deliverables and Schedule` with a structured current-deliverable status table.
- [x] Added and resolved the table-numbering follow-up comment.
- [x] Renumbered the inserted status table as `Table 1` and shifted later table captions through `Table 23`.
- [x] Resolved the original status-table feedback comment.
- [x] Added Section 4 portfolio-level synthesis after the policy-count/panel overview.
- [x] Resolved the Section 4 why-it-matters synthesis comment.
- [x] Removed extra blank paragraphs from the new Section 4 synthesis so the doc uses normal paragraph spacing.
- [x] Added EDA interpretation sentences for product composition, age/cost pressure, and premium-vs-claim exposure.
- [x] Resolved the EDA interpretation feedback comment.

## Phase 0: Inventory And Rules

- [x] Inventory active comments and classify them by effort/risk.
- [x] Track Google Doc edits separately from repo code changes because the live Google Doc is the report source of truth.
- [x] Record source-of-truth and evidence rules in `DECISIONS.md`.

## Phase 1: Main Report Feedback Cleanup

- [x] Status table: make completed work, evidence/output, current status, and remaining work explicit.
- [x] Table numbering: add status table as `Table 1` and update later table captions.
- [x] Section 4 synthesis: add 2-3 portfolio-level takeaways after the data overview.
- [x] EDA interpretation: add concise why-it-matters sentences after major EDA figures/tables and resolve comment `AAAB6ZeO7Js`.
- [ ] Dashboard deliverable framing: add one clean dashboard screenshot and 2-3 sentences tying dashboard, models, segmentation, action queues, and stakeholder decisions together; resolve comment `AAAB6ZeO7J8`.
- [ ] Recommendations / remaining work: make Section 10 action steps explicit with next step, owner/team role, evidence needed, and final-deliverable impact; resolve comment `AAAB6ZeO7KA`.

## Phase 2: Evidence-Backed Additions

- [ ] Model comparison: benchmark Logistic Regression, Decision Tree, Random Forest, and XGBoost on the same split, then add AUC/recall/precision/F1/threshold table; resolve comment `AAAB6ZeO7J0`.
- [ ] Action-list screenshot: verify whether current report image is full-portfolio or fast-preview sample; replace or relabel and resolve comment `AAAB6O99cO8`.
- [ ] Alignment consistency: confirm whether table/figure titles are centered consistently after the latest edits; resolve or keep comment `AAAB6O99cQU` with a reason.

## Phase 3: Final Deliverables

- [ ] CEO-ready Executive Summary: create separate summary doc if the team wants to address comment `AAAB6ZeO7Jc` now.
- [ ] Final pass: check open comments, table captions, section spacing, and whether newly added prose sounds student-authored rather than over-polished.
- [ ] Optional: export PDF and visually inspect page breaks/captions before submission.

## Lower-Priority Cleanup

- [ ] Update tracker with any new comments created in the Google Doc after this session.
- [ ] If report claims are changed based on new model runs, update repo artifacts and cite exact output files in the report.

## Explicit Exceptions

- [~] Do not mark the Executive Summary comment complete just because the main report has an executive-summary section. The comment asks for a separate CEO-ready document.
- [~] Do not resolve model-comparison feedback until benchmark metrics are actually produced or verified from repo output.

## Inventory Snapshot

| Item | Bucket | Status | Owner/System | Source Of Truth | Verification Required | Last Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Live Google Doc `P2 Initial Findings Report - Team 54 v2` | Phase 1 | `[-]` | Google Docs | Doc ID `1qROBjYtdrFew8WJbOoN8efbboXYSREfCGxY6kXNmxnU` | Read doc text/comments after every edit | 2026-05-12 text/comment checks | Main report source of truth |
| Section 3 status table | Phase 1 | `[x]` | Google Docs | Live doc | Confirm table caption and resolved comment | 2026-05-12 `Table 1` verified | Inserted table replaces loose status prose |
| Section 4 synthesis | Phase 1 | `[x]` | Google Docs | Live doc | Confirm prose exists and comment resolved | 2026-05-12 export text check | Extra blank paragraphs removed |
| EDA interpretation comments | Phase 1 | `[x]` | Google Docs | Live doc and `output/` figures/tables | Confirm added sentences and resolved comment | 2026-05-12 connector text/comment checks | Added targeted interpretation notes and resolved `AAAB6ZeO7Js` |
| Dashboard deliverable comment | Phase 1 | `[ ]` | Google Docs + repo outputs | `dashboard.py`, `streamlit_app.py`, `output/dashboard_screenshots_euro/` | Screenshot must match report claim | Pending | Next recommended item |
| Model comparison comment | Phase 2 | `[ ]` | Repo + Google Docs | `src/models.py`, `src/train_pipeline.py`, `output/model_summary.json` | Run or verify benchmarks | Pending | Heavier task |
| CEO-ready Executive Summary | Phase 3 | `[ ]` | Google Docs/Drive | New separate doc if created | Confirm doc exists and comment resolved | Pending | Keep separate from main report |

## Session Closeout Checklist

- [x] Update statuses for every item touched this session.
- [x] Add verification evidence to `VERIFICATION.md`.
- [x] Add new classification, scope, or exception decisions to `DECISIONS.md`.
- [ ] Add commit hashes and pushed state when applicable.
- [x] Refresh `Current phase` and `Next recommended item`.
- [x] Update `../INDEX.md` if it exists.

## Sensitive Information Rule

- Do not store live passwords, PINs, access tokens, recovery codes, PHI, or other secrets here.
- Use source paths, doc IDs, ticket IDs, or redacted values instead.

## Session Notes

- Created on `2026-05-12`.
- The tracker lives in the repo, but several tracked edits happen in the live Google Doc. Verify live doc state before marking doc items done.
