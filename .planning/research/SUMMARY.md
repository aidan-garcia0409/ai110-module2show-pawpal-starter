# Project Research Summary

**Project:** PawPal — Python OOP Pet Care Scheduling App with Streamlit UI
**Domain:** Python OOP school project / scheduling application
**Researched:** 2026-03-19
**Confidence:** HIGH

## Executive Summary

PawPal is a Python OOP assignment that produces a pet care scheduling application backed by pure-Python dataclasses and a priority-based scheduler, surfaced through a Streamlit UI and validated with pytest unit tests. The project is tightly scoped by assignment requirements: Python 3.11+, Streamlit for UI, pytest for testing, and a UML class diagram as a deliverable. The recommended approach is a clean three-layer separation — domain models (Pet, Owner, Task) in `models.py`, scheduling logic (Scheduler, Schedule, TimeBlock) in `scheduler.py`, and all Streamlit code isolated in `app.py`. The entire domain layer must be importable by pytest without a running Streamlit server; this is the single most important architectural constraint.

The dependency chain is deterministic and must be respected: Pet → Task → Owner → TimeBlock → Schedule → Scheduler → app.py wiring → tests. Building in this order means every layer is testable before the next is built. The default task library (`defaults.py`) and UML diagram should be drafted early — the UML is a design tool, not documentation, and the task library reduces demo friction. The scope is intentionally narrow: single-day scheduling, no persistence, no auth, no LLM features.

The primary risks are structural rather than algorithmic. Defining domain classes inside `app.py`, storing priority as a raw string without a sort map, and doing `datetime.time` arithmetic directly are the three failure modes most likely to sink test coverage. All three are preventable with patterns documented in PITFALLS.md and ARCHITECTURE.md. Addressing them in Phase 1 and Phase 2 eliminates compounding problems in later phases.

---

## Key Findings

### Recommended Stack

The stack is almost entirely Python standard library. Streamlit (>=1.30) is assignment-mandated for UI; pytest (>=7.0) is assignment-mandated for testing. Everything else — `dataclasses`, `datetime`, `enum` — is stdlib with no additional installs. Mermaid (inline in Markdown) is the right choice for the UML diagram: zero install, renders in GitHub and VS Code, and version-controlled alongside the code. No database, no ORM, no external API clients are needed or appropriate for this scope.

**Core technologies:**
- Python 3.11+: Runtime — `dataclasses` and `datetime.time` behave correctly; widely installed in school environments
- Streamlit >=1.30: UI layer — assignment-mandated; handles session state, widget reruns, and display without JavaScript
- pytest >=7.0: Unit testing — assignment-mandated; simple function-based tests, no boilerplate
- `dataclasses` (stdlib): Domain models — eliminates `__init__` boilerplate for Pet, Owner, Task, TimeBlock, Schedule
- `datetime` / `timedelta` (stdlib): Time arithmetic — `datetime.datetime` for internal arithmetic, `datetime.time` for display only
- `enum` (stdlib): Priority ordering — `Priority(str, Enum)` gives correct sort ordering and Streamlit selectbox compatibility
- Mermaid (inline Markdown): UML diagram — zero install, version-controlled, renders in GitHub

### Expected Features

The assignment defines a clear must-have set centered on domain models, a working scheduler algorithm, Streamlit wiring, pytest coverage, and a UML diagram. Differentiators are all low-effort and should only be added after table stakes are complete.

**Must have (table stakes):**
- Pet, Owner, Task dataclasses — everything else depends on these
- `Scheduler.generate_schedule()` with priority sort and time-budget fit check
- Frequency expansion — tasks with `frequency > 1` produce multiple TimeBlocks
- `Schedule.explain()` — human-readable plan string
- Default task library keyed by species (`"dog"`, `"cat"`, `"other"`)
- Streamlit "Generate schedule" button wired to real Scheduler backend
- Schedule displayed as time-blocked list (start time, task title, pet name, reason)
- pytest unit tests for all domain classes (importable without Streamlit)
- Mermaid UML class diagram
- `reflection.md` completed

**Should have (differentiators — add after table stakes):**
- Auto-populate tasks from species library when a pet is added — reduces demo friction
- "Skipped tasks" section showing what didn't fit — explains scheduler decisions transparently
- Priority badge coloring in schedule display — visual polish
- Time-budget validation warning before scheduling — prevents confusing empty output
- Available hours input in the UI — makes time budget configurable by user

**Defer (out of scope per PROJECT.md):**
- Care history, database persistence, or authentication
- Multi-day scheduling
- LLM-generated suggestions
- Abstract base classes or deep inheritance hierarchies
- pytest for the Streamlit UI layer
- Real-time updates

### Architecture Approach

The architecture is a strict three-layer separation: `app.py` (Streamlit presentation only) → `scheduler.py` (orchestration and algorithm) → `models.py` + `defaults.py` (pure Python domain). The cardinal rule is that nothing below `app.py` imports Streamlit. The trickiest integration point is the session state bridge: `st.session_state.tasks` stores plain dicts, but `Scheduler` requires `Task` objects. This conversion must happen entirely inside `app.py`, keeping domain classes clean and independently testable.

**Major components:**
1. `models.py` — Pet, Owner, Task dataclasses; pure Python; zero Streamlit imports; fully testable
2. `scheduler.py` — Scheduler (generate_schedule algorithm), Schedule (block container + explain()), TimeBlock (start/end time + reason); pure Python; zero Streamlit imports
3. `defaults.py` — Default task library dict keyed by species; pure data; no logic
4. `app.py` — All Streamlit code; converts session_state dicts to domain objects; calls Scheduler; renders Schedule
5. `tests/` — test_models.py and test_scheduler.py; import only from domain modules, never from app.py

### Critical Pitfalls

1. **Domain classes defined in app.py** — pytest cannot import them without Streamlit, causing all tests to fail. Prevention: establish the file boundary on day one; Pet and Scheduler never appear in app.py.
2. **Priority sorted as raw string** — alphabetical sort puts "high" < "low" < "medium", scheduling wrong tasks first. Prevention: use `PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}` as the sort key, or a `Priority(str, Enum)` with explicit ordering.
3. **`datetime.time` arithmetic** — `datetime.time` objects do not support addition; all blocks get the same start time or the code crashes. Prevention: use `datetime.datetime` internally for elapsed-time tracking, convert to `.time()` only for display.
4. **Frequency not expanded before sorting** — tasks with `frequency=3` appear only once in the schedule. Prevention: expand frequency copies as the first step in `generate_schedule()`, before the priority sort.
5. **Session state dicts passed directly to Scheduler** — type inconsistency throughout; tests require dict construction rather than object construction. Prevention: convert dicts → Task objects in app.py using the bridge pattern before calling Scheduler.

---

## Implications for Roadmap

Based on research, the dependency chain dictates a clear three-phase structure. Each phase must be stable and tested before the next begins.

### Phase 1: Domain Models and Design Foundation

**Rationale:** Pet, Owner, and Task are the root of every dependency. Nothing else can be built or tested without them. The UML diagram should be drafted here — it is a design tool, and drafting it before coding reveals relationship issues early. Establishing the file-separation boundary in Phase 1 prevents the most critical pitfall from ever occurring.

**Delivers:** `models.py` with Pet, Owner, Task dataclasses; Mermaid UML class diagram; `defaults.py` default task library; `tests/test_models.py` passing.

**Addresses (from FEATURES.md):** Pet/Owner/Task dataclasses, default task library, UML deliverable.

**Avoids (from PITFALLS.md):** Domain classes in app.py (boundary set here); UML left until last (drafted here).

### Phase 2: Scheduler Algorithm and Core Logic

**Rationale:** Scheduler depends on fully defined domain objects from Phase 1. The three critical algorithmic pitfalls (priority sort, datetime arithmetic, frequency expansion) all live in this phase and must be solved correctly before UI wiring begins — a broken scheduler discovered in Phase 3 is much harder to debug inside Streamlit's rerun model.

**Delivers:** `scheduler.py` with Scheduler, Schedule, TimeBlock; correct priority sort with PRIORITY_ORDER map; frequency expansion before sort; datetime.datetime-based time arithmetic; `Schedule.explain()`; `tests/test_scheduler.py` passing.

**Uses (from STACK.md):** `datetime`/`timedelta` stdlib, `enum` stdlib, `dataclasses` stdlib, pytest.

**Implements (from ARCHITECTURE.md):** Application layer (Scheduler orchestration); scheduling path data flow.

**Avoids (from PITFALLS.md):** Priority raw-string sort; datetime.time arithmetic; frequency not expanded before sort; tests importing Streamlit.

### Phase 3: Streamlit Wiring and App Integration

**Rationale:** app.py is the last layer to build because it depends on everything below it. The session state bridge pattern (converting dicts → domain objects) must be applied here deliberately. Empty-schedule feedback and session state guard patterns prevent confusing demo behavior.

**Delivers:** `app.py` fully wired — "Generate schedule" button calls real Scheduler; schedule displayed as time-blocked list with pet names and reasons; skipped tasks shown; empty-schedule warning; session state guards for pets and tasks; available hours input.

**Addresses (from FEATURES.md):** Streamlit UI wiring, multi-pet schedule display, "skipped tasks" section, time-budget validation warning.

**Avoids (from PITFALLS.md):** Dicts passed to Scheduler; empty schedule with no feedback; session state re-run bugs.

### Phase 4: Polish, Deliverables, and Submission

**Rationale:** Differentiator features (auto-populate from species library, priority badge coloring) and final deliverables (`reflection.md`, README cleanup) should come last. Adding polish before core logic is stable wastes time if scheduler behavior changes.

**Delivers:** Auto-populate tasks from species library on pet add; priority badge coloring; completed `reflection.md`; README with rendered Mermaid diagram; final pytest run clean.

**Addresses (from FEATURES.md):** Remaining differentiators; all assignment deliverables.

### Phase Ordering Rationale

- The Pet → Task → Owner → Scheduler dependency chain from ARCHITECTURE.md directly maps to Phase 1 → Phase 2 build order.
- Keeping Streamlit wiring in Phase 3 (after domain logic is tested) matches the architectural constraint that pytest must be able to import domain classes independently — a constraint that is easiest to enforce when app.py is written last.
- The three critical pitfalls (priority sort, datetime arithmetic, frequency expansion) are all Phase 2 concerns — solving them before Phase 3 means they are validated by pytest before Streamlit's rerun loop makes debugging harder.
- Differentiators and submission deliverables in Phase 4 prevent scope creep from blocking core functionality.

### Research Flags

Phases with standard patterns (skip additional research-phase):
- **Phase 1:** Dataclasses and Mermaid UML are well-documented with established patterns; no research needed.
- **Phase 2:** Scheduler algorithm is a standard priority-sort + time-tracking loop; pitfall prevention patterns are fully documented in PITFALLS.md.
- **Phase 3:** Streamlit session state bridge pattern is documented in ARCHITECTURE.md; no novel integration needed.
- **Phase 4:** Reflection and README are pure writing; no research needed.

No phases require a `/gsd:research-phase` deep dive. The domain is small, the stack is stdlib-heavy, and all patterns are documented.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Assignment requirements constrain choices; stdlib modules have authoritative docs; no external APIs |
| Features | HIGH | PROJECT.md defines the feature set; table stakes are unambiguous; differentiators are clearly bounded |
| Architecture | HIGH | Three-layer separation is a standard Python pattern; session state bridge is well-understood |
| Pitfalls | HIGH | Pitfalls are concrete, reproducible failure modes with specific prevention patterns; not speculative |

**Overall confidence:** HIGH

### Gaps to Address

- **Available hours default value:** Research did not specify the default value for `Owner.available_hours`. The starter app likely has an 8-hour default; validate against `app.py` during Phase 3 wiring.
- **Starter app session state shape:** The exact shape of `st.session_state.tasks` dicts in the starter depends on the existing `app.py` code. Inspect before building the Phase 3 bridge to avoid type mismatches.
- **`reflection.md` prompt content:** The specific questions in `reflection.md` were not researched. Locate the file in the starter and read the prompts before Phase 4.

---

## Sources

### Primary (HIGH confidence)
- Python 3.11 `dataclasses` stdlib docs — dataclass decorator usage, field defaults
- Python 3.11 `datetime` stdlib docs — `datetime.time`, `datetime.datetime`, `timedelta` arithmetic
- Python 3.11 `enum` stdlib docs — `str, Enum` mixin for string-comparable enums
- Streamlit >=1.30 docs — `st.session_state`, widget reruns, session state initialization guard pattern
- pytest >=7.0 docs — function-based test syntax, fixture patterns

### Secondary (MEDIUM confidence)
- Streamlit community patterns — session state dict-to-object bridge; established by repeated community usage
- Mermaid `classDiagram` docs — class relationship syntax; confirmed zero-install in GitHub/VS Code

### Tertiary (LOW confidence)
- Default available_hours value — inferred as 8 hours from common scheduling app conventions; validate against starter app

---

*Research completed: 2026-03-19*
*Ready for roadmap: yes*
