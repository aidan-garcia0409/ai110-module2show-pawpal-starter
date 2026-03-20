---
phase: 3
slug: app-integration
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-20
---

# Phase 3 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest >= 7.0 |
| **Config file** | none — pytest discovers tests/ directory automatically |
| **Quick run command** | `pytest tests/ -x -q` |
| **Full suite command** | `pytest tests/ -v` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/ -x -q`
- **After every plan wave:** Run `pytest tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green + manual walkthrough of all 5 success criteria
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 3-01-01 | 01 | 1 | APP-05 | manual | n/a — UI selectbox not pytest-testable | — | ⬜ pending |
| 3-01-02 | 01 | 1 | APP-01 | manual + auto | `pytest tests/ -x -q` (domain tests remain green) | ✅ | ⬜ pending |
| 3-01-03 | 01 | 1 | APP-02, APP-03, APP-04 | manual | n/a — Streamlit rendering out of scope per REQUIREMENTS.md | — | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements.* No new test files needed — REQUIREMENTS.md explicitly declares pytest for Streamlit UI layer as Out of Scope. All APP-0x requirements are verified by manual browser testing. Existing domain tests in `tests/` serve as the automated gate.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| "Generate schedule" button calls real Scheduler | APP-01 | Streamlit session state is not pytest-friendly (REQUIREMENTS.md Out of Scope) | Run `streamlit run app.py`, fill form with owner/pet/tasks, click Generate — verify schedule rows appear |
| Schedule shows start time, task title, pet name, reason | APP-02 | UI rendering not testable in pytest | Confirm table shows all 4 columns with correct data |
| Skipped tasks shown in separate section | APP-03 | UI rendering not testable in pytest | Add tasks exceeding 8h total; verify "Skipped Tasks" section appears |
| Empty schedule shows warning message | APP-04 | UI rendering not testable in pytest | Click Generate with no tasks — confirm st.warning message appears instead of blank |
| Species restricted to "dog" and "cat" only | APP-05 | Selectbox options not testable in pytest | Open app, verify species dropdown has exactly 2 options: dog, cat |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
