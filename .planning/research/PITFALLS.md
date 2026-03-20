# Pitfalls Research

**Project:** PawPal — Python OOP + Streamlit School Project
**Researched:** 2026-03-19

---

## Critical Pitfalls

### 1. Defining Domain Classes Inside app.py

**Warning signs:** `class Pet:` or `class Scheduler:` appears in `app.py`
**Why it happens:** Feels convenient — everything in one file
**Consequence:** pytest cannot import Pet/Scheduler without importing Streamlit. Streamlit throws errors when imported outside a running server. **All tests fail.**
**Prevention:** Domain classes live in `models.py` and `scheduler.py`. `app.py` only imports them.
**Phase:** Phase 1 (models) — establish this boundary from day one

---

### 2. Scheduler Receiving Dicts Instead of Domain Objects

**Warning signs:** `scheduler.tasks[0]["priority"]` instead of `scheduler.tasks[0].priority`
**Why it happens:** `st.session_state.tasks` stores plain dicts — easy to pass them straight through
**Consequence:** Scheduler code is littered with dict key access; tests require constructing dicts instead of objects; type inconsistency throughout
**Prevention:** Convert session_state dicts → `Task` objects in `app.py` before calling `Scheduler`. The conversion bridge pattern (see ARCHITECTURE.md) handles this cleanly.
**Phase:** Phase 3 (app wiring)

---

### 3. Empty Schedule with No Explanation

**Warning signs:** Generate schedule → blank output, no error message
**Why it happens:** Time budget too low, or all tasks skip silently
**Consequence:** Confusing demo; looks broken
**Prevention:**
- Always show "Scheduled: X tasks" and "Skipped: Y tasks (time budget exceeded)"
- Add a sanity check: if `len(schedule.blocks) == 0`, show `st.warning("No tasks fit in the available time. Try increasing available hours or reducing task durations.")`
**Phase:** Phase 3 (app wiring)

---

### 4. Frequency > 1 Tasks Not Expanded Before Sorting

**Warning signs:** A task with `frequency=3` appears only once in the schedule
**Why it happens:** Scheduler sorts tasks, then checks frequency — but the copy loop runs after scheduling
**Consequence:** Repeating tasks (e.g., feeding 3x/day) only get one slot
**Prevention:** Expand frequency **before** sorting. Create `frequency` copies of the task (with distinct labels like "Feeding (1/3)") as the first step in `generate_schedule()`.
**Phase:** Phase 2 (scheduler)

---

### 5. Priority Comparison Fails with String Values

**Warning signs:** `sorted(tasks, key=lambda t: t.priority)` sorts alphabetically ("high" < "low" < "medium")
**Why it happens:** Priority stored as raw string, Python sorts strings lexicographically
**Consequence:** Tasks scheduled in wrong order — "low" priority tasks before "high" ones
**Prevention:** Use a priority map for sorting:
```python
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
sorted_tasks = sorted(tasks, key=lambda t: PRIORITY_ORDER[t.priority])
```
Or use `Priority(str, Enum)` with explicit ordering.
**Phase:** Phase 2 (scheduler)

---

### 6. Start Time Arithmetic Errors

**Warning signs:** Schedule shows "8:00am, 8:00am, 8:00am" or times go past midnight
**Why it happens:** `datetime.time` doesn't support addition — can't do `start_time + timedelta(minutes=20)`
**Consequence:** All time blocks have the same start time, or code crashes
**Prevention:** Use `datetime.datetime` internally for time arithmetic, convert to `datetime.time` only for display:
```python
from datetime import datetime, timedelta
current = datetime.combine(datetime.today(), datetime.strptime("08:00", "%H:%M").time())
# add duration
current += timedelta(minutes=task.duration_minutes)
# extract time for display
block_end = current.time()
```
**Phase:** Phase 2 (scheduler)

---

### 7. Tests That Import Streamlit

**Warning signs:** `import streamlit` appears in any test file
**Why it happens:** Test file imports from `app.py` which imports `streamlit`
**Consequence:** Tests may fail in CI or when run outside a Streamlit context
**Prevention:** Test files only import from `models.py`, `scheduler.py`, `defaults.py` — never from `app.py`
**Phase:** Phase 2-3 (tests)

---

### 8. UML Diagram Left Until Last

**Warning signs:** "I'll draw the diagram after the code is done"
**Why it happens:** Feels like documentation, not design
**Consequence:** UML doesn't match the actual implementation; last-minute scramble
**Prevention:** Draft the UML class diagram **before** writing code (it IS the design). Update it if classes change during implementation. Mermaid in a README is version-controlled and easy to update.
**Phase:** Phase 1 (models design)

---

### 9. Session State Pet/Task Mismatch on Re-run

**Warning signs:** Adding a second pet resets the task list
**Why it happens:** Streamlit reruns the entire script on each widget interaction; session state initialization guard missing
**Consequence:** Users lose their entered data
**Prevention:** Always use the guard pattern:
```python
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "pets" not in st.session_state:
    st.session_state.pets = []
```
The starter already does this for tasks — extend the pattern to pets.
**Phase:** Phase 3 (app wiring)

---

## Pitfall Priority Summary

| Pitfall | Severity | Phase to Address |
|---------|----------|-----------------|
| Domain classes in app.py | 🔴 Critical | Phase 1 |
| Priority sort with raw strings | 🔴 Critical | Phase 2 |
| `datetime.time` arithmetic | 🔴 Critical | Phase 2 |
| Frequency not expanded before sort | 🟠 High | Phase 2 |
| Dicts passed to Scheduler | 🟠 High | Phase 3 |
| Empty schedule no feedback | 🟡 Medium | Phase 3 |
| Session state re-run bugs | 🟡 Medium | Phase 3 |
| UML left until last | 🟡 Medium | Phase 1 |
| Tests importing Streamlit | 🟡 Medium | Phase 2-3 |
