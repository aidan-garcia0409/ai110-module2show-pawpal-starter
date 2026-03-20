# Roadmap: PawPal

## Overview

PawPal is built in four sequential phases that follow the natural dependency chain of the codebase. Phase 1 establishes the pure-Python domain layer (models, task library, UML diagram) that everything else depends on. Phase 2 builds the scheduler algorithm on top of those models and validates it with pytest before any Streamlit code is written. Phase 3 wires the working backend into the existing Streamlit UI so the app generates and displays a real schedule. Phase 4 completes the assignment deliverables (reflection document, README cleanup, final test run).

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Domain Models** - Define Pet, Owner, Task dataclasses, default task library, and Mermaid UML diagram
- [ ] **Phase 2: Scheduler Algorithm** - Implement Scheduler, Schedule, TimeBlock with correct priority sort, frequency expansion, and time arithmetic
- [ ] **Phase 3: App Integration** - Wire scheduler backend into Streamlit UI with schedule display, skipped tasks, and edge case feedback
- [ ] **Phase 4: Submission Deliverables** - Complete reflection.md and finalize README

## Phase Details

### Phase 1: Domain Models
**Goal**: The pure-Python domain layer exists, is importable without Streamlit, and matches the class design in PROJECT.md
**Depends on**: Nothing (first phase)
**Requirements**: MOD-01, MOD-02, MOD-03, MOD-04, LIB-01, DEL-02
**Success Criteria** (what must be TRUE):
  1. Pet, Owner, and Task dataclasses can be imported from models.py in a plain Python script with no Streamlit dependency
  2. Priority comparison produces the correct order (high before medium before low) — not alphabetical
  3. Default task library returns pre-loaded tasks for "dog" and "cat" species
  4. Mermaid UML class diagram in README renders all six classes and their relationships correctly
**Plans**: 2 plans

Plans:
- [ ] 01-01-PLAN.md — Test scaffold (Wave 0) + models.py dataclasses, PRIORITY_ORDER, and get_default_tasks
- [ ] 01-02-PLAN.md — Mermaid UML class diagram in README.md

### Phase 2: Scheduler Algorithm
**Goal**: Scheduler.generate_schedule() produces a correct, time-bounded Schedule with per-block reasons — validated entirely by pytest before any Streamlit code is touched
**Depends on**: Phase 1
**Requirements**: SCHED-01, SCHED-02, SCHED-03, SCHED-04, SCHED-05, DEL-01
**Success Criteria** (what must be TRUE):
  1. pytest test suite runs and passes with zero Streamlit imports in test files
  2. Given tasks of mixed priority, the generated schedule places high-priority tasks before medium and medium before low
  3. A task with frequency=2 produces two separate TimeBlocks in the schedule
  4. Tasks that exceed the remaining time budget are excluded from the schedule (not silently dropped without record)
  5. Schedule.explain() returns a readable string listing each scheduled block with start time, end time, and reason
**Plans**: TBD

### Phase 3: App Integration
**Goal**: The Streamlit app generates and displays a real time-blocked schedule when the user clicks "Generate schedule"
**Depends on**: Phase 2
**Requirements**: APP-01, APP-02, APP-03, APP-04, APP-05
**Success Criteria** (what must be TRUE):
  1. Clicking "Generate schedule" calls the real Scheduler backend and renders the result — the button is no longer stubbed
  2. The schedule display shows each block as a row with start time, task title, pet name, and reason
  3. Tasks that did not fit the time budget are shown in a separate "Skipped tasks" section
  4. Submitting with no tasks (or a schedule that produces zero blocks) shows a warning message instead of a blank section
  5. Pet species input is restricted to "dog" and "cat" — "other" is not an available option
**Plans**: TBD

### Phase 4: Submission Deliverables
**Goal**: All assignment deliverables are complete and the project is ready to submit
**Depends on**: Phase 3
**Requirements**: DEL-03
**Success Criteria** (what must be TRUE):
  1. reflection.md answers all prompts provided in the starter file
  2. Final pytest run is clean (all tests pass, no warnings about missing imports)
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Domain Models | 0/2 | Not started | - |
| 2. Scheduler Algorithm | 0/TBD | Not started | - |
| 3. App Integration | 0/TBD | Not started | - |
| 4. Submission Deliverables | 0/TBD | Not started | - |
