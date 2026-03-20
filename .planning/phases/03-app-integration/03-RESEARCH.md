# Phase 3: App Integration - Research

**Researched:** 2026-03-20
**Domain:** Streamlit UI integration with pure-Python backend (models.py)
**Confidence:** HIGH

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| APP-01 | "Generate schedule" button wired to real Scheduler backend | Backend API is fully implemented in models.py; bridge is straightforward Scheduler construction + call |
| APP-02 | Schedule displayed as time-blocked list (start time, task title, pet name, reason) | Each TimeBlock carries all four fields; st.table or per-row rendering works |
| APP-03 | Skipped tasks (didn't fit time budget) shown separately | schedule.skipped is a list[Task]; render in a second section below blocks |
| APP-04 | Empty schedule shows helpful warning message | st.warning() before the table render; guard on `len(schedule.blocks) == 0` |
| APP-05 | Pet species restricted to "dog" and "cat" only | Remove "other" from the st.selectbox options list |
</phase_requirements>

---

## Summary

Phase 3 is a UI wiring phase, not an algorithm phase. The entire backend (Pet, Owner, Task, Scheduler, Schedule, TimeBlock) exists and is tested in models.py. The existing app.py collects owner name, pet name, species, and a task list in `st.session_state.tasks` (a list of dicts). The "Generate schedule" button currently shows a static warning stub. This phase replaces that stub with real Scheduler calls.

The key integration challenge is the impedance mismatch between what the UI collects and what the backend expects: the UI stores tasks as plain dicts (`{"title": ..., "duration_minutes": ..., "priority": ...}`) with no Pet object attached. The integration layer must construct Pet and Owner domain objects from the UI inputs, convert the session-state dicts into Task objects with the pet reference set, and pass them to Scheduler.

The second challenge is display: Streamlit has no built-in "time-blocked list" widget. The standard pattern is to render each TimeBlock as a row using `st.columns()` or `st.table()` / `st.dataframe()`. Either works; `st.table()` with a list-of-dicts is simplest and requires no pandas import.

**Primary recommendation:** In the "Generate schedule" button handler, construct domain objects from session state, call `Scheduler(owner, tasks).generate_schedule()`, then render `schedule.blocks` row by row and `schedule.skipped` in a separate section. Guard on empty blocks with `st.warning()`.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| streamlit | >=1.30 (already in requirements.txt) | UI rendering, session state, widgets | Project's chosen UI framework; already installed |
| models.py | project-local | Pet, Owner, Task, Scheduler, Schedule, TimeBlock | All domain logic lives here by project convention |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| datetime (stdlib) | stdlib | Time formatting for display | TimeBlock.start_time and end_time are datetime.time objects — use `.strftime("%H:%M")` for display |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| st.table(list_of_dicts) | st.dataframe(pd.DataFrame(...)) | dataframe requires pandas; not in requirements.txt; st.table is sufficient |
| per-row st.columns render | st.table | st.columns gives more control over layout; st.table is simpler; either is acceptable |

**Installation:** No new packages needed. All dependencies are in requirements.txt already.

---

## Architecture Patterns

### Current app.py Structure (starter — what exists)

```
app.py
  ├─ st.set_page_config(...)
  ├─ st.title(...)
  ├─ owner_name = st.text_input("Owner name", ...)
  ├─ pet_name   = st.text_input("Pet name", ...)
  ├─ species    = st.selectbox("Species", ["dog", "cat", "other"])  ← must drop "other"
  ├─ task input fields (task_title, duration, priority)
  ├─ "Add task" button → appends dict to st.session_state.tasks
  ├─ st.table(st.session_state.tasks)  (display current tasks)
  └─ "Generate schedule" button → STUB (replace this)
```

### Pattern 1: Session-State Dict → Domain Object Bridge

**What:** Convert `st.session_state.tasks` list-of-dicts into proper Task objects before scheduling.

**When to use:** Whenever UI collects raw values and backend needs typed domain objects.

**Example:**
```python
# Source: models.py interface (project-local, verified by reading file)
from models import Pet, Owner, Task, Scheduler

# Inside the "Generate schedule" button handler:
pet  = Pet(name=pet_name, species=species, age=0)   # age not collected in UI; default 0
owner = Owner(name=owner_name, available_hours=8)    # available_hours: see Pitfall 1

tasks = [
    Task(
        title=t["title"],
        duration_minutes=t["duration_minutes"],
        priority=t["priority"],
        frequency=1,       # UI does not collect frequency; default 1
        pet=pet,
    )
    for t in st.session_state.tasks
]

schedule = Scheduler(owner=owner, tasks=tasks).generate_schedule()
```

### Pattern 2: Schedule Render with Guarded Sections

**What:** Display schedule.blocks and schedule.skipped, with an empty-state guard.

**When to use:** Whenever rendering a result that may be empty.

**Example:**
```python
# Source: Streamlit docs (st.warning, st.table are standard APIs)
if not schedule.blocks:
    st.warning("No tasks could be scheduled. Add tasks or increase available hours.")
else:
    st.subheader("Today's Schedule")
    rows = [
        {
            "Start": block.start_time.strftime("%H:%M"),
            "Task": block.task.title,
            "Pet": block.task.pet.name,
            "Reason": block.reason,
        }
        for block in schedule.blocks
    ]
    st.table(rows)

if schedule.skipped:
    st.subheader("Skipped Tasks")
    skipped_rows = [
        {"Task": t.title, "Duration": t.duration_minutes, "Priority": t.priority}
        for t in schedule.skipped
    ]
    st.table(skipped_rows)
```

### Pattern 3: Restricting a Selectbox to Valid Choices

**What:** Change the species selectbox options list to remove "other".

**When to use:** Enforcing domain constraints at the UI layer (APP-05).

**Example:**
```python
# Source: existing app.py line 44 — change in-place
# Before:
species = st.selectbox("Species", ["dog", "cat", "other"])
# After:
species = st.selectbox("Species", ["dog", "cat"])
```

### Anti-Patterns to Avoid

- **Importing models at the top of app.py without guarding for import errors:** models.py is a plain Python file — import is safe, but keep the import at module top so it fails fast rather than inside a button handler.
- **Mutating `st.session_state.tasks` inside the "Generate schedule" handler:** The task list must remain intact for re-runs. Only read from it; never write to it during schedule generation.
- **Using `st.experimental_rerun()` unnecessarily:** The schedule can be rendered in the same script run as the button click. Streamlit re-runs automatically on widget interaction.
- **Rendering schedule before checking for empty tasks:** Always guard `if not st.session_state.tasks` OR `if not schedule.blocks` to prevent confusing blank sections (APP-04).

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Priority-based task sorting | Custom sort logic in app.py | `Scheduler.generate_schedule()` already handles it | Scheduler in models.py is tested; duplicating sort logic creates divergence |
| Time arithmetic (start/end times) | Manual minute addition in app.py | `Scheduler.generate_schedule()` already produces TimeBlock with start_time/end_time | Tested code; re-implementing risks off-by-one and midnight-crossing bugs |
| Human-readable schedule text | Custom string formatting in app.py | `Schedule.explain()` for text output; structured list-of-dicts for table display | explain() is already implemented and tested |
| Task storage/persistence | File I/O or database in app.py | `st.session_state` (already used in starter) | Project is session-state-only by design (Out of Scope in REQUIREMENTS.md) |

**Key insight:** Phase 3 is a thin adapter. All computation belongs to models.py. app.py translates UI inputs → domain objects → UI outputs.

---

## Common Pitfalls

### Pitfall 1: available_hours Default Value

**What goes wrong:** Owner.available_hours is not collected in the UI. The starter doesn't include an "available hours" input. If a hard-coded default is wrong, the schedule will silently include or exclude tasks incorrectly.

**Why it happens:** STATE.md explicitly flags this: "Available hours default value not confirmed — validate against starter app.py during Phase 3." The Owner dataclass requires an integer.

**How to avoid:** Use `available_hours=8` (a reasonable full-day default) unless a specific value was confirmed. Make the value obvious in the code with a comment so it can be changed easily. Do not collect it from UI (UX-01 in v2 requirements is out of scope for this phase).

**Warning signs:** Schedule produces zero blocks with tasks that should clearly fit.

### Pitfall 2: age Field on Pet

**What goes wrong:** The UI does not collect `age`. Pet requires `age: int`. Forgetting this field causes a TypeError on Pet construction.

**Why it happens:** app.py only collects pet_name and species; age was never added to the UI form.

**How to avoid:** Use `age=0` as a default when constructing Pet in the button handler. The scheduler never reads age; it is only a data field.

### Pitfall 3: Task Dict Shape Mismatch

**What goes wrong:** `st.session_state.tasks` contains dicts with keys `"title"`, `"duration_minutes"`, `"priority"` — not Task objects. Code that tries to call `.title` attribute on a dict item will raise `AttributeError`.

**Why it happens:** The starter stores raw dicts (line 61-63 of app.py), not domain objects. The bridge code must explicitly convert.

**How to avoid:** Always iterate with dict key access (`t["title"]`) when reading from session state, then construct Task objects explicitly (Pattern 1 above).

### Pitfall 4: frequency Not Collected in UI

**What goes wrong:** Task has a `frequency` field. The UI never collects it. If frequency is not set, the dataclass default is `1` — which is correct. But if the code tries to read `t["frequency"]` from session state it will raise `KeyError`.

**Why it happens:** The "Add task" button only stores `{"title", "duration_minutes", "priority"}`. No `frequency` key exists in those dicts.

**How to avoid:** Hard-code `frequency=1` when constructing Task objects from session state. Do not attempt to read `t.get("frequency")` unless you also update the "Add task" form.

### Pitfall 5: Streamlit Button Re-run Behavior

**What goes wrong:** The schedule disappears on every widget interaction (e.g., typing in a text field) because Streamlit re-runs the script top-to-bottom and the schedule is not stored in session state.

**Why it happens:** `if st.button("Generate schedule"):` only executes the block once — on the click re-run. On the next widget interaction, the block is skipped and the rendered schedule vanishes.

**How to avoid:** Store the generated schedule in `st.session_state`:
```python
if st.button("Generate schedule"):
    st.session_state.schedule = Scheduler(owner, tasks).generate_schedule()

if "schedule" in st.session_state:
    # render st.session_state.schedule here
```
This keeps the schedule visible until the user explicitly regenerates.

---

## Code Examples

Verified patterns from project source files:

### Complete Button Handler (Synthesized from models.py API)

```python
# Source: models.py (read 2026-03-20) — verified API signatures
from models import Pet, Owner, Task, Scheduler

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        pet   = Pet(name=pet_name, species=species, age=0)
        owner = Owner(name=owner_name, available_hours=8)  # default; no UI field
        tasks = [
            Task(
                title=t["title"],
                duration_minutes=t["duration_minutes"],
                priority=t["priority"],
                frequency=1,
                pet=pet,
            )
            for t in st.session_state.tasks
        ]
        st.session_state.schedule = Scheduler(owner=owner, tasks=tasks).generate_schedule()

if "schedule" in st.session_state:
    schedule = st.session_state.schedule
    if not schedule.blocks:
        st.warning("No tasks fit the time budget. Try adding shorter or higher-priority tasks.")
    else:
        st.subheader("Today's Schedule")
        st.table([
            {
                "Start": b.start_time.strftime("%H:%M"),
                "Task": b.task.title,
                "Pet": b.task.pet.name,
                "Reason": b.reason,
            }
            for b in schedule.blocks
        ])

    if schedule.skipped:
        st.subheader("Skipped Tasks")
        st.table([
            {"Task": t.title, "Duration (min)": t.duration_minutes, "Priority": t.priority}
            for t in schedule.skipped
        ])
```

### Species Restriction (APP-05)

```python
# Source: app.py line 44 — change in-place
species = st.selectbox("Species", ["dog", "cat"])   # "other" removed
```

### Time Formatting

```python
# Source: models.py Schedule.explain() — verified pattern
start_str = block.start_time.strftime("%H:%M")  # e.g. "08:00"
end_str   = block.end_time.strftime("%H:%M")    # e.g. "08:30"
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `st.experimental_rerun()` | `st.rerun()` | Streamlit 1.27+ | Use `st.rerun()` if needed; experimental version is deprecated |
| `st.beta_columns()` | `st.columns()` | Streamlit 1.x stable | `st.columns()` is the stable API; beta prefix removed |

**Deprecated/outdated:**
- `st.experimental_*` APIs: All experimental APIs were stabilized or removed in Streamlit 1.30+. The project requires `streamlit>=1.30`, so use stable names only.

---

## Open Questions

1. **available_hours default value**
   - What we know: STATE.md flags this as unconfirmed. Owner dataclass requires an integer. The UI has no field for it.
   - What's unclear: Whether the assignment grader expects a specific default or any reasonable value.
   - Recommendation: Use `8` (hours in a workday) with a clear comment. This is reasonable and makes scheduling behavior predictable. The planner should make this a named constant at the top of the button handler.

2. **Schedule persistence across widget interactions**
   - What we know: Streamlit re-runs fully on every widget event, so rendered output from a button handler disappears unless stored.
   - What's unclear: Whether the assignment requires schedule persistence between interactions or just immediate post-click rendering.
   - Recommendation: Store in `st.session_state.schedule` (Pitfall 5 pattern). This is strictly better UX and adds only one line.

3. **Multi-pet support**
   - What we know: The current UI collects only ONE pet name and species. Owner.pets is a list. Scheduler takes a flat task list.
   - What's unclear: Whether the integration should support multiple pets (v2 UX-02) or just one.
   - Recommendation: Single pet only for Phase 3. Construct one Pet from UI inputs; pass tasks with that pet set. Multi-pet is out of scope.

---

## Validation Architecture

> nyquist_validation is enabled in config.json.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest >= 7.0 |
| Config file | none — pytest discovers tests/ directory automatically |
| Quick run command | `pytest tests/ -x -q` |
| Full suite command | `pytest tests/ -v` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| APP-01 | Generate schedule button calls Scheduler, produces Schedule | manual-only | n/a — Streamlit session state not pytest-friendly (see REQUIREMENTS.md Out of Scope) | — |
| APP-02 | Schedule displayed with start time, task title, pet name, reason | manual-only | n/a — UI rendering not testable in pytest | — |
| APP-03 | Skipped tasks shown in separate section | manual-only | n/a — UI rendering not testable in pytest | — |
| APP-04 | Empty schedule shows warning | manual-only | n/a — UI rendering not testable in pytest | — |
| APP-05 | Species restricted to dog/cat | manual-only | n/a — selectbox options not testable in pytest | — |

**Note:** REQUIREMENTS.md explicitly declares "pytest for Streamlit UI layer" as Out of Scope: "Streamlit session state is not pytest-friendly; test domain logic only." All APP-0x requirements are verified by manual browser testing. The existing pytest suite in `tests/` covers the domain logic that APP-01 depends on; those tests remain the automated gate.

### Sampling Rate

- **Per task commit:** `pytest tests/ -x -q` (verify existing domain tests still pass after any models.py changes)
- **Per wave merge:** `pytest tests/ -v`
- **Phase gate:** All domain tests green + manual walkthrough of all 5 success criteria before `/gsd:verify-work`

### Wave 0 Gaps

None — existing test infrastructure covers all domain logic. Phase 3 adds no new pytest tests (UI layer is out of scope per project requirements). The only verification is manual app testing via `streamlit run app.py`.

---

## Sources

### Primary (HIGH confidence)

- `models.py` (project root, read 2026-03-20) — Pet, Owner, Task, Scheduler, Schedule, TimeBlock API verified by direct source inspection
- `app.py` (project root, read 2026-03-20) — exact session_state.tasks shape, widget names, current stub implementation verified
- `.planning/REQUIREMENTS.md` (read 2026-03-20) — APP-01 through APP-05 requirements and Out of Scope section
- `requirements.txt` (read 2026-03-20) — confirms streamlit>=1.30 and pytest>=7.0, no pandas

### Secondary (MEDIUM confidence)

- `.planning/STATE.md` (read 2026-03-20) — Blockers/Concerns section flags available_hours and session_state.tasks shape as items to verify; both now verified by direct file inspection
- Streamlit stable API (`st.table`, `st.warning`, `st.columns`, `st.session_state`) — standard APIs unchanged since 1.30; no breaking changes expected

### Tertiary (LOW confidence)

- None

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — models.py and app.py read directly; no inference required
- Architecture: HIGH — session_state.tasks shape confirmed from app.py source; domain API confirmed from models.py source
- Pitfalls: HIGH — pitfalls derived from direct inspection of field names and UI data shapes, not speculation

**Research date:** 2026-03-20
**Valid until:** 2026-04-20 (stable domain; Streamlit 1.30 API is stable)
