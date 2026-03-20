# PawPal

## What This Is

PawPal is a pet care planning assistant built in Streamlit. It lets a pet owner add their pets and care tasks, then generates a time-blocked daily schedule across all pets — prioritizing tasks by urgency and fitting them within the owner's available hours. Each scheduled block includes an explanation of why it was chosen.

## Core Value

The scheduler automatically builds a complete, time-blocked care plan for all your pets that respects priorities and time budget — so no care task gets missed.

## Requirements

### Validated

- ✓ Streamlit app with basic task input UI (title, duration, priority) — existing starter
- ✓ Owner name and pet name inputs — existing starter
- ✓ Session state management for task list — existing starter

### Active

- [ ] Pet profile model with name, species, age, and preferences
- [ ] Owner model with available_hours time budget and list of pets
- [ ] Task model with title, duration, priority, frequency, and pet assignment
- [ ] Default task library (common care tasks pre-loaded per species)
- [ ] Scheduler class: sort by priority, schedule tasks that fit time budget
- [ ] Repeating tasks (frequency > 1) assigned multiple time blocks
- [ ] Schedule + TimeBlock output with start/end times per block
- [ ] Per-block explanation: why this task was scheduled
- [ ] Time-blocked schedule display wired into app.py
- [ ] UML class diagram showing all relationships
- [ ] pytest unit tests for models and scheduling logic
- [ ] Reflection document completed

### Out of Scope

- Care history / activity log — profile only, no past-care tracking (v2)
- Per-schedule one-pet filtering — all pets scheduled together always
- Time slots across multiple days — single day schedule only
- Authentication — local single-user app
- Database persistence — session state only

## Context

This is a Codepath AI110 Module 2 school project. The starter app (`app.py`) provides a working Streamlit UI with task input, session state for tasks, and a stubbed "Generate schedule" button. The student's job is to design and implement the backend classes and wire them in.

**Deliverables required by the assignment:**
1. Working Streamlit app (existing UI + implemented backend)
2. UML class diagram
3. pytest unit tests
4. Reflection document (`reflection.md`)

**Existing UI inputs available in app.py:**
- Owner name (`st.text_input`)
- Pet name (`st.text_input`) + species (`st.selectbox`)
- Task: title, duration (minutes), priority (low/medium/high)
- "Add task" button → `st.session_state.tasks` list
- "Generate schedule" button (currently stubbed)

## Class Design

```
Owner
  - name: str
  - available_hours: int          # time budget for the day
  - pets: list[Pet]               # composition: Owner has many Pets

Pet
  - name: str
  - species: str                  # "dog" | "cat" | "other"
  - age: int
  - preferences: dict             # e.g., {"walk_before": "noon"}

Task
  - title: str
  - duration_minutes: int
  - priority: str                 # "low" | "medium" | "high"
  - frequency: int                # times per day (1 = once, 2 = twice, etc.)
  - pet: Pet                      # each task belongs to one pet

Scheduler
  - owner: Owner
  - tasks: list[Task]
  + generate_schedule() -> Schedule
    # Algorithm: sort all tasks by priority (high→med→low),
    # schedule each in order if it fits remaining time budget.
    # Repeating tasks get scheduled frequency times.

Schedule
  - blocks: list[TimeBlock]
  + explain() -> str              # full schedule summary

TimeBlock
  - task: Task
  - start_time: time
  - end_time: time
  - reason: str                   # e.g., "High priority, fits 20min morning window"
```

**UML relationships:**
- `Owner` 1 ──< `Pet` (composition)
- `Pet` 1 ──< `Task` (composition)
- `Scheduler` uses `Owner` + `list[Task]`
- `Scheduler` produces `Schedule`
- `Schedule` 1 ──< `TimeBlock`
- `TimeBlock` references `Task`

## Constraints

- **Tech stack**: Python + Streamlit — must stay in this stack (assignment requirement)
- **Scope**: Single-day schedule only
- **Persistence**: Streamlit session_state only — no database
- **Tests**: pytest required — domain logic must be testable independently of Streamlit

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Task belongs to one Pet | Simplifies UML and scheduling output labeling | — Pending |
| Algorithm: priority-sort then fit | Simple to implement and test; matches assignment constraints | — Pending |
| Owner holds available_hours | Time budget is an owner-level concept, not per-pet | — Pending |
| Default task library per species | Reduces manual entry; shows system design depth | — Pending |

---
*Last updated: 2026-03-19 after initialization*
