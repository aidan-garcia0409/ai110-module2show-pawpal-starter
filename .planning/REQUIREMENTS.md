# Requirements: PawPal

**Defined:** 2026-03-20
**Core Value:** Algorithmically generate a time-blocked daily care schedule across all pets that respects priorities and time budget — so no care task gets missed.

---

## v1 Requirements

### Models

- [ ] **MOD-01**: Pet dataclass with name, species (`"dog"` | `"cat"`), age, and preferences dict
- [ ] **MOD-02**: Owner dataclass with name, available_hours (time budget), and pets list
- [ ] **MOD-03**: Task dataclass with title, duration_minutes, priority, frequency (times/day), and pet reference
- [ ] **MOD-04**: Priority uses correct sort ordering (not raw string comparison)

### Scheduler

- [ ] **SCHED-01**: Scheduler takes Owner + task list and produces a Schedule
- [ ] **SCHED-02**: Tasks sorted by priority (high → medium → low), scheduled greedily if they fit remaining time budget
- [ ] **SCHED-03**: Tasks with frequency > 1 expanded to multiple TimeBlocks before sorting
- [ ] **SCHED-04**: TimeBlock has start_time, end_time, and reason string
- [ ] **SCHED-05**: Schedule.explain() returns human-readable plan summary

### Task Library

- [ ] **LIB-01**: Default task library with common care tasks pre-loaded for dogs and cats (no "other" category)

### App Integration

- [ ] **APP-01**: "Generate schedule" button wired to real Scheduler backend
- [ ] **APP-02**: Schedule displayed as time-blocked list (start time, task title, pet name, reason)
- [ ] **APP-03**: Skipped tasks (didn't fit time budget) shown separately
- [ ] **APP-04**: Empty schedule shows helpful warning message
- [ ] **APP-05**: Pet species restricted to "dog" and "cat" only

### Deliverables

- [ ] **DEL-01**: pytest unit tests for models and scheduler (importable without Streamlit)
- [ ] **DEL-02**: Mermaid UML class diagram in README
- [ ] **DEL-03**: reflection.md completed

---

## v2 Requirements

### UX Enhancements

- **UX-01**: Available hours configurable by user in the UI (currently uses Owner default)
- **UX-02**: Auto-populate default tasks when a pet is added (based on species)
- **UX-03**: Priority badge coloring in schedule display

---

## Out of Scope

| Feature | Reason |
|---------|--------|
| "Other" species | Scope decision — keeping library focused on dogs and cats |
| Care history / activity log | v2+ — profile only, no past-care tracking |
| Database persistence | Session state only — no database for this assignment |
| Authentication | Single-user local app |
| Multi-day scheduling | Single day schedule only |
| LLM-generated suggestions | Wrong abstraction for an OOP class assignment |
| pytest for Streamlit UI layer | Streamlit session state is not pytest-friendly; test domain logic only |

---

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| MOD-01 | Phase 1 | Pending |
| MOD-02 | Phase 1 | Pending |
| MOD-03 | Phase 1 | Pending |
| MOD-04 | Phase 1 | Pending |
| LIB-01 | Phase 1 | Pending |
| DEL-02 | Phase 1 | Pending |
| SCHED-01 | Phase 2 | Pending |
| SCHED-02 | Phase 2 | Pending |
| SCHED-03 | Phase 2 | Pending |
| SCHED-04 | Phase 2 | Pending |
| SCHED-05 | Phase 2 | Pending |
| DEL-01 | Phase 2 | Pending |
| APP-01 | Phase 3 | Pending |
| APP-02 | Phase 3 | Pending |
| APP-03 | Phase 3 | Pending |
| APP-04 | Phase 3 | Pending |
| APP-05 | Phase 3 | Pending |
| DEL-03 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 18 total
- Mapped to phases: 18
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-20*
*Last updated: 2026-03-20 after initial definition*
