# Architecture Research

**Project:** PawPal — Python OOP Scheduling App
**Researched:** 2026-03-19

---

## Recommended Architecture

Three-layer separation:

```
Presentation  →  app.py          (Streamlit only — NO domain logic)
Application   →  scheduler.py    (orchestration, algorithm)
Domain        →  pawpal/         (pure Python classes, zero Streamlit)
```

**Cardinal rule:** Nothing below `app.py` imports Streamlit. Ever.

---

## Module Structure

```
app.py                    # Streamlit UI only — imports from pawpal/
pawpal/
    __init__.py
    models.py             # Pet, Owner, Task dataclasses
    scheduler.py          # Scheduler, Schedule, TimeBlock
    defaults.py           # Default task library keyed by species
tests/
    __init__.py
    test_models.py        # Tests for Pet, Owner, Task
    test_scheduler.py     # Tests for Scheduler algorithm
```

**Simpler alternative** (acceptable for this scope):
```
app.py
models.py       # Pet, Owner, Task
scheduler.py    # Scheduler, Schedule, TimeBlock
defaults.py     # Default task library
tests/
    test_models.py
    test_scheduler.py
```

Either structure works — the flat version is fine for a school project.

---

## Data Flow

### Input path
```
Streamlit widgets
  → app.py reads st.session_state
  → constructs Pet objects (from pet name/species inputs)
  → constructs Task objects (from task list in session state)
  → constructs Owner object (name + available_hours + pets)
  → passes Owner + tasks to Scheduler(owner, tasks)
```

### Scheduling path
```
Scheduler.generate_schedule()
  → expand repeating tasks (frequency > 1 → multiple Task copies)
  → sort all tasks by priority (high → medium → low)
  → iterate tasks, track elapsed_minutes
  → for each task: if elapsed + duration <= available_minutes → schedule it
  → create TimeBlock(task, start_time, end_time, reason)
  → return Schedule(blocks=[...])
```

### Output path
```
app.py receives Schedule
  → iterates schedule.blocks
  → renders each TimeBlock: start_time, task.title, task.pet.name, reason
  → st.table() or st.write() per block
```

---

## Build Order (Dependency-Driven)

| Step | What | Why |
|------|------|-----|
| 1 | `Pet` | No dependencies — start here |
| 2 | `Task` | Needs Pet reference |
| 3 | `Owner` | Needs Pet list |
| 4 | `TimeBlock` | Needs Task reference |
| 5 | `Schedule` | Needs list of TimeBlocks |
| 6 | `Scheduler` | Needs Owner + list of Tasks |
| 7 | `defaults.py` | Needs Pet + Task constructors |
| 8 | `app.py` wiring | Assembles all domain objects, calls Scheduler |
| 9 | `tests/` | Validates each layer independently |

Test as you go — write `test_models.py` after step 3, `test_scheduler.py` after step 6.

---

## Class Relationships

```
Owner "1" *-- "many" Pet : has
Pet "1" *-- "many" Task : has
Scheduler --> Owner : uses
Scheduler --> Schedule : creates
Schedule "1" *-- "many" TimeBlock : contains
TimeBlock --> Task : references
```

---

## Key Anti-Patterns to Avoid

| Anti-pattern | Consequence | Prevention |
|---|---|---|
| Domain classes import Streamlit | pytest can't import them — tests fail | Keep models.py/scheduler.py import-free of streamlit |
| Scheduling logic written inline in app.py | Untestable; fails the pytest deliverable | All algorithm logic lives in Scheduler class |
| Keeping tasks as plain dicts into Scheduler | Type inconsistency; can't call task.priority | Convert session_state dicts → Task objects in app.py before passing to Scheduler |
| Constructing domain objects inside Scheduler | Couples Scheduler to UI inputs | Scheduler receives already-constructed objects |
| All classes in one file | Fine at this scale; monitor if it grows | Optional: split models.py later if needed |

---

## Streamlit Session State Bridge

The trickiest integration point: `st.session_state.tasks` stores dicts, but `Scheduler` needs `Task` objects.

**Pattern to use in app.py:**
```python
# Convert session_state dicts → domain objects before scheduling
pet = Pet(name=pet_name, species=species, age=0, preferences={})
tasks = [
    Task(
        title=t["title"],
        duration_minutes=t["duration_minutes"],
        priority=t["priority"],
        frequency=1,
        pet=pet
    )
    for t in st.session_state.tasks
]
owner = Owner(name=owner_name, available_hours=8, pets=[pet])
scheduler = Scheduler(owner=owner, tasks=tasks)
schedule = scheduler.generate_schedule()
```

This conversion happens entirely in `app.py` — domain classes stay clean.
