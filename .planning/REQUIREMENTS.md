# Requirements: PawPal

**Defined:** 2026-03-20
**Core Value:** Algorithmically generate a time-blocked daily care schedule across all pets that respects priorities and time budget — so no care task gets missed.

---

## v1 Requirements

### Models

- [x] **MOD-01**: Pet dataclass with name, species (`"dog"` | `"cat"`), age, and preferences dict
- [x] **MOD-02**: Owner dataclass with name, available_hours (time budget), and pets list
- [x] **MOD-03**: Task dataclass with title, duration_minutes, priority, frequency (times/day), and pet reference
- [x] **MOD-04**: Priority uses correct sort ordering (not raw string comparison)

### Scheduler

- [x] **SCHED-01**: Scheduler takes Owner + task list and produces a Schedule
- [x] **SCHED-02**: Tasks sorted by priority (high → medium → low), scheduled greedily if they fit remaining time budget
- [x] **SCHED-03**: Tasks with frequency > 1 expanded to multiple TimeBlocks before sorting
- [x] **SCHED-04**: TimeBlock has start_time, end_time, and reason string
- [x] **SCHED-05**: Schedule.explain() returns human-readable plan summary

### Task Library

- [x] **LIB-01**: Default task library with common care tasks pre-loaded for dogs and cats (no "other" category)

### App Integration

- [x] **APP-01**: "Generate schedule" button wired to real Scheduler backend
- [x] **APP-02**: Schedule displayed as time-blocked list (start time, task title, pet name, reason)
- [x] **APP-03**: Skipped tasks (didn't fit time budget) shown separately
- [x] **APP-04**: Empty schedule shows helpful warning message
- [x] **APP-05**: Pet species restricted to "dog" and "cat" only

### Deliverables

- [x] **DEL-01**: pytest unit tests for models and scheduler (importable without Streamlit)
- [x] **DEL-02**: Mermaid UML class diagram in README
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
| MOD-01 | Phase 1 | Complete |
| MOD-02 | Phase 1 | Complete |
| MOD-03 | Phase 1 | Complete |
| MOD-04 | Phase 1 | Complete |
| LIB-01 | Phase 1 | Complete |
| DEL-02 | Phase 1 | Complete |
| SCHED-01 | Phase 2 | Complete |
| SCHED-02 | Phase 2 | Complete |
| SCHED-03 | Phase 2 | Complete |
| SCHED-04 | Phase 2 | Complete |
| SCHED-05 | Phase 2 | Complete |
| DEL-01 | Phase 2 | Complete |
| APP-01 | Phase 3 | Complete |
| APP-02 | Phase 3 | Complete |
| APP-03 | Phase 3 | Complete |
| APP-04 | Phase 3 | Complete |
| APP-05 | Phase 3 | Complete |
| DEL-03 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 18 total
- Mapped to phases: 18
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-20*
*Last updated: 2026-03-20 after roadmap creation*
