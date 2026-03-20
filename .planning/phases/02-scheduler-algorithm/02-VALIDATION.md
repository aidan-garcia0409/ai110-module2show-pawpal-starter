---
phase: 2
slug: scheduler-algorithm
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-20
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.0.2 |
| **Config file** | none — pytest discovers `tests/` by convention |
| **Quick run command** | `.venv/bin/python -m pytest tests/test_scheduler.py -x` |
| **Full suite command** | `.venv/bin/python -m pytest tests/ -v` |
| **Estimated runtime** | ~2 seconds |

---

## Sampling Rate

- **After every task commit:** Run `.venv/bin/python -m pytest tests/test_scheduler.py -x`
- **After every plan wave:** Run `.venv/bin/python -m pytest tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** ~2 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 2-01-01 | 01 | 0 | DEL-01 | unit | `.venv/bin/python -m pytest tests/test_scheduler.py -x` | ❌ W0 | ⬜ pending |
| 2-01-02 | 01 | 1 | SCHED-01 | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_generate_schedule_returns_schedule -x` | ❌ W0 | ⬜ pending |
| 2-01-03 | 01 | 1 | SCHED-04 | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_timeblock_has_start_end_reason -x` | ❌ W0 | ⬜ pending |
| 2-01-04 | 01 | 1 | SCHED-04 | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_timeblock_end_after_start -x` | ❌ W0 | ⬜ pending |
| 2-02-01 | 02 | 2 | SCHED-02 | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_high_priority_scheduled_before_low -x` | ❌ W0 | ⬜ pending |
| 2-02-02 | 02 | 2 | SCHED-02 | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_task_exceeding_budget_goes_to_skipped -x` | ❌ W0 | ⬜ pending |
| 2-02-03 | 02 | 2 | SCHED-03 | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_frequency_2_produces_two_blocks -x` | ❌ W0 | ⬜ pending |
| 2-02-04 | 02 | 2 | SCHED-05 | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_explain_returns_string -x` | ❌ W0 | ⬜ pending |
| 2-02-05 | 02 | 2 | SCHED-05 | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_explain_contains_task_title -x` | ❌ W0 | ⬜ pending |
| 2-02-06 | 02 | 2 | SCHED-05 | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_explain_empty_schedule -x` | ❌ W0 | ⬜ pending |
| 2-03-01 | 03 | 3 | DEL-01 | integration | `.venv/bin/python -m pytest tests/ -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_scheduler.py` — stubs/full tests for SCHED-01, SCHED-02, SCHED-03, SCHED-04, SCHED-05, DEL-01
- [ ] `models.py` — add `import datetime` and `TimeBlock`, `Schedule`, `Scheduler` dataclasses

*No new framework install needed — pytest 9.0.2 already installed in `.venv`*

---

## Manual-Only Verifications

*All phase behaviors have automated verification.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 2s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
