# Features Research

**Project:** PawPal — Pet Care Scheduling App
**Researched:** 2026-03-19

---

## Table Stakes (Must-Have for Assignment Completion)

### Domain Models
- **Pet dataclass** — name, species, age, preferences dict
- **Owner dataclass** — name, available_hours, pets list
- **Task dataclass** — title, duration_minutes, priority, frequency, pet reference
- *Dependency: everything else builds on these*

### Scheduler
- **`Scheduler.generate_schedule()`** — priority sort (high→med→low) + time-budget fit check
- **Repeating task expansion** — `frequency > 1` produces multiple `TimeBlock`s (e.g., feed 3x/day = 3 blocks)
- **Schedule + TimeBlock output** — `start_time`, `end_time`, `reason` per block
- **`Schedule.explain()`** — summary method returning human-readable plan string

### Task Library
- **Default task library** — dict keyed by species (`"dog"`, `"cat"`, `"other"`) with common care tasks pre-populated
- *Reduces manual input; shows thoughtful system design*

### App Integration
- **Wire `app.py` "Generate schedule" button** to real Scheduler backend
- **Display time-blocked schedule** in Streamlit (table or list with start times + reasons)
- **Multi-pet awareness** — schedule covers all pets, tasks labeled by pet name

### Deliverables
- **pytest unit tests** for all domain classes (importable without Streamlit)
- **UML class diagram** (Mermaid recommended — renders in GitHub/VS Code)
- **`reflection.md`** completed

---

## Differentiators (Add Only After Table Stakes Are Done)

| Feature | Value | Complexity |
|---------|-------|------------|
| Auto-populate tasks from species library when pet is added | Reduces friction, shows smart defaults | Low |
| "Skipped tasks" section showing what didn't fit | Explains scheduler decisions transparently | Low |
| Priority badge coloring in schedule display | Visual polish for demo | Low |
| Time-budget validation warning before scheduling | Prevents confusing empty schedule | Low |
| Available hours input in the UI | Makes time budget configurable by user | Low |

---

## Anti-Features (Explicitly Do NOT Build)

| Feature | Why Not |
|---------|---------|
| Care history / database / auth | Out of scope per PROJECT.md; wrong abstraction level |
| Multi-day scheduling | Scope-creep; complicates time-block math significantly |
| LLM-generated suggestions | Wrong abstraction for an OOP class assignment |
| Abstract base classes / deep inheritance | Adds UML noise without meeting requirements |
| pytest for Streamlit UI layer | Session state is not pytest-friendly; test domain logic only |
| Real-time updates / websockets | Streamlit doesn't support this pattern simply |

---

## Critical Dependency Chain

```
Pet → Task → Scheduler → Schedule/TimeBlock → app.py display
```

Build in this order. Nothing downstream works without upstream being tested first.

---

## Feature Complexity Notes

| Feature | Effort | Notes |
|---------|--------|-------|
| Pet/Owner/Task dataclasses | Low | ~30 lines of code total |
| Default task library | Low | Dict literal, no logic |
| Scheduler algorithm | Medium | Sorting + time tracking loop |
| Frequency expansion | Low-Medium | Loop multiplier on tasks before scheduling |
| TimeBlock with reason | Low | String formatting from task properties |
| Streamlit wiring | Medium | Translating session state dicts → domain objects |
| pytest tests | Medium | Need fixtures for Owner/Pet/Task setup |
| UML diagram | Low | Mermaid classDiagram ~20 lines |
