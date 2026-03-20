# Phase 1: Domain Models - Context

**Gathered:** 2026-03-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Define Pet, Owner, Task dataclasses and a default task library as a pure-Python module (`models.py`) importable without Streamlit. Produce a Mermaid UML class diagram in the README. Scheduler logic and app wiring are separate phases.

</domain>

<decisions>
## Implementation Decisions

### Preferences dict
- `Pet.preferences` is an empty dict placeholder in Phase 1 — content will be populated in Phase 2+ when the scheduler needs to read it
- Use `field(default_factory=dict)` as the dataclass default — caller does not need to pass it explicitly

### Default task library
- Implemented as a module-level function: `get_default_tasks(pet: Pet) -> list[Task]`
- Takes a Pet object; returns Task instances pre-assigned to that pet (real Task objects, not raw dicts)
- 6–8 tasks per species (dog and cat only — no "other")
- Tasks carry realistic priorities: mix of high/medium/low
- Some tasks have `frequency > 1` (e.g., feeding=2, water refresh=2) to exercise that model field
- Example dog tasks: morning walk, feeding (×2), water refresh (×2), evening walk, playtime, grooming
- Example cat tasks: feeding (×2), water refresh (×2), litter box, playtime, brushing, nail trim

### UML diagram
- Attributes + key methods shown (e.g., `generate_schedule()`, `explain()`, `get_default_tasks()`)
- Lives in README.md as a new `## Class Diagram` section
- Format: one brief intro sentence + fenced Mermaid code block

### Claude's Discretion
- Priority representation: sort-map dict (`PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}`) or `Priority` enum — either works, choose whichever makes the Phase 2 comparisons cleaner
- Exact task durations in the default library (e.g., walk=30min, feeding=10min)
- Exact intro sentence wording for the UML section

</decisions>

<specifics>
## Specific Ideas

- No specific requirements — open to standard approaches for class structure and Mermaid syntax

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- None yet — `models.py` does not exist; this phase creates it from scratch

### Established Patterns
- `app.py` stores tasks as raw dicts: `{"title": str, "duration_minutes": int, "priority": str}` — Phase 3 will need a bridge between these dicts and Task objects; Phase 1 just defines the dataclass
- `app.py` uses `@dataclass`-unfriendly session state (plain dicts) — models must be independently constructable without app context

### Integration Points
- `models.py` must be importable with a plain `import models` (no Streamlit, no app.py dependency)
- Phase 2 Scheduler will import `Pet`, `Owner`, `Task`, `Schedule`, `TimeBlock` from `models.py`
- Phase 3 will import `get_default_tasks` and the model classes to build the real UI flow

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 01-domain-models*
*Context gathered: 2026-03-20*
