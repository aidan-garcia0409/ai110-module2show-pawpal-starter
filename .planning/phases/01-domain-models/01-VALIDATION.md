---
phase: 1
slug: domain-models
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-20
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.0.2 |
| **Config file** | none — Wave 0 creates tests/ directory |
| **Quick run command** | `python -m pytest tests/test_models.py -x` |
| **Full suite command** | `python -m pytest tests/ -v` |
| **Estimated runtime** | ~2 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_models.py -x`
- **After every plan wave:** Run `python -m pytest tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 2 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 1-01-01 | 01 | 0 | MOD-01 | unit | `python -m pytest tests/test_models.py::test_pet_importable_without_streamlit -x` | ❌ W0 | ⬜ pending |
| 1-01-02 | 01 | 0 | MOD-02 | unit | `python -m pytest tests/test_models.py::test_owner_fields -x` | ❌ W0 | ⬜ pending |
| 1-01-03 | 01 | 0 | MOD-03 | unit | `python -m pytest tests/test_models.py::test_task_fields -x` | ❌ W0 | ⬜ pending |
| 1-01-04 | 01 | 1 | MOD-04 | unit | `python -m pytest tests/test_models.py::test_priority_order_correct -x` | ❌ W0 | ⬜ pending |
| 1-01-05 | 01 | 1 | LIB-01 | unit | `python -m pytest tests/test_models.py::test_get_default_tasks_dog_returns_tasks tests/test_models.py::test_get_default_tasks_cat_returns_tasks -x` | ❌ W0 | ⬜ pending |
| 1-01-06 | 01 | 1 | LIB-01 | unit | `python -m pytest tests/test_models.py::test_get_default_tasks_dog_has_frequency_gt_1 -x` | ❌ W0 | ⬜ pending |
| 1-01-07 | 01 | 2 | DEL-02 | manual | Open README.md on GitHub — verify Mermaid diagram renders all six classes | N/A | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_models.py` — stubs for MOD-01, MOD-02, MOD-03, MOD-04, LIB-01
- [ ] `tests/__init__.py` — empty file for package discovery (conventional)

*No pytest config file needed — pytest 9.0.2 discovers `tests/` by convention.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Mermaid class diagram renders all six classes in README | DEL-02 | GitHub renders Mermaid client-side; no CLI tool can verify visual rendering | Push to GitHub, open README.md, confirm diagram shows Owner, Pet, Task, Scheduler, Schedule, TimeBlock with correct relationships |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 2s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
