# Phase 2: Scheduler Algorithm - Research

**Researched:** 2026-03-20
**Domain:** Python greedy scheduling algorithm, datetime arithmetic, dataclasses, pytest
**Confidence:** HIGH

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| SCHED-01 | Scheduler takes Owner + task list and produces a Schedule | `Scheduler(owner, tasks)` dataclass or plain class; `generate_schedule()` returns a `Schedule` instance |
| SCHED-02 | Tasks sorted by priority (high → medium → low), scheduled greedily if they fit remaining time budget | `sorted(tasks, key=lambda t: PRIORITY_ORDER[t.priority])` then iterate; track `remaining_minutes = owner.available_hours * 60`; skip if `task.duration_minutes > remaining_minutes` |
| SCHED-03 | Tasks with frequency > 1 expanded to multiple TimeBlocks before sorting | Pre-expand: `[task] * task.frequency` (or explicit loop) produces N copies before the sort step; each copy becomes its own TimeBlock |
| SCHED-04 | TimeBlock has start_time, end_time, and reason string | `@dataclass TimeBlock` with `datetime.time start_time`, `datetime.time end_time`, `str reason`; use `datetime.datetime` for arithmetic, `.time()` for storage |
| SCHED-05 | Schedule.explain() returns human-readable plan summary | `Schedule.explain()` iterates `self.blocks`, formats each as `"{start} - {end}: {task.title} ({task.pet.name}) — {reason}"`, joins with newlines |
| DEL-01 | pytest unit tests for models and scheduler (importable without Streamlit) | New `tests/test_scheduler.py` — imports only from `models.py`; no Streamlit dependency; covers all five SCHED requirements |
</phase_requirements>

---

## Summary

Phase 2 adds three new classes to `models.py` — `TimeBlock`, `Schedule`, and `Scheduler` — and a `tests/test_scheduler.py` file. No new third-party libraries are needed. All algorithms use stdlib `datetime` and the `PRIORITY_ORDER` dict already defined in Phase 1.

The core algorithm is a greedy scheduler: expand tasks with `frequency > 1` into N copies, sort all copies by priority (using `PRIORITY_ORDER`), then iterate and assign each task to a time slot if it fits within the owner's remaining time budget. Tasks that don't fit go into a `skipped` list on the Schedule object. `TimeBlock` tracks the wall-clock start and end time of each assigned task. `Schedule.explain()` produces a readable string from all blocks.

The critical design choice is where the new classes live: they belong in `models.py` alongside Pet, Owner, and Task so that `import models` in test files remains a single, Streamlit-free import. Do not create a separate `scheduler.py` unless there is a strong structural reason — the phase 3 planner will import all domain objects from `models.py`, and splitting them across files adds complexity with no benefit at this project scale.

**Primary recommendation:** Add `TimeBlock`, `Schedule`, and `Scheduler` to the existing `models.py`. Implement `generate_schedule()` as a greedy frequency-expand → sort → fit loop. Write `tests/test_scheduler.py` covering all five SCHED requirements and DEL-01. Start day at 08:00 by convention.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `dataclasses` (stdlib) | Python 3.7+ (3.14.3 in .venv) | Define TimeBlock, Schedule, Scheduler | Already used for Pet/Owner/Task; consistent pattern; zero new imports |
| `datetime` (stdlib) | Python 3.3+ | Time arithmetic for TimeBlock start/end | Correct handling of minute-rollover across hours; `.time()` for display, `datetime.datetime` for arithmetic |
| `pytest` | 9.0.2 (installed in .venv) | Unit tests for scheduler logic | Already installed and configured; 8 tests passing |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `dataclasses.field` | stdlib | Mutable defaults (`blocks: list`, `skipped: list`) on Schedule | Required for any list/dict default in a dataclass — same rule as Phase 1 |
| `datetime.timedelta` | stdlib | Add `duration_minutes` to a running clock | `current_time += timedelta(minutes=task.duration_minutes)` — cleaner than manual minute/hour arithmetic |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Add classes to `models.py` | Separate `scheduler.py` | Separate file adds an import and a new test-isolation concern; models.py already has all domain objects; stay simple |
| `datetime.time` arithmetic | Manual int minutes math | `datetime.time` doesn't support `+`; must use `datetime.datetime` for arithmetic then call `.time()` — stdlib-correct approach |
| Greedy sort-then-fit | Backtracking / optimal packing | Requirements say "greedy if they fit" — don't over-engineer; greedy is the spec |

**Installation:**

No new installs required — all dependencies already in `.venv`:
```bash
# Already installed:
# Python 3.14.3
# pytest 9.0.2
# streamlit 1.55.0 (not used in this phase)
```

---

## Architecture Patterns

### Recommended Project Structure

```
pawpal-starter/
├── app.py                   # Streamlit UI (do not modify in Phase 2)
├── models.py                # Phase 2 output: add TimeBlock, Schedule, Scheduler here
├── tests/
│   ├── __init__.py          # existing
│   ├── test_models.py       # existing — 8 tests passing, do not break
│   └── test_scheduler.py    # Wave 0 gap — create in this phase
├── requirements.txt
└── README.md
```

### Pattern 1: TimeBlock Dataclass

**What:** `TimeBlock` stores the task reference, wall-clock start and end times (as `datetime.time`), and a reason string explaining why this task was scheduled.

**When to use:** One TimeBlock per scheduled task occurrence.

**Example:**
```python
# Source: stdlib dataclasses docs + STATE.md decision
from dataclasses import dataclass
import datetime

@dataclass
class TimeBlock:
    task: "Task"
    start_time: datetime.time
    end_time: datetime.time
    reason: str
```

### Pattern 2: Schedule Dataclass with explain()

**What:** `Schedule` holds two lists — `blocks` (scheduled tasks) and `skipped` (tasks that didn't fit). `explain()` returns a formatted string suitable for display.

**When to use:** `Scheduler.generate_schedule()` constructs and returns a Schedule.

**Example:**
```python
@dataclass
class Schedule:
    blocks: list = field(default_factory=list)   # list[TimeBlock]
    skipped: list = field(default_factory=list)  # list[Task]

    def explain(self) -> str:
        if not self.blocks:
            return "No tasks scheduled."
        lines = []
        for block in self.blocks:
            start = block.start_time.strftime("%H:%M")
            end   = block.end_time.strftime("%H:%M")
            lines.append(
                f"{start} - {end}: {block.task.title} "
                f"({block.task.pet.name}) — {block.reason}"
            )
        return "\n".join(lines)
```

### Pattern 3: Scheduler with generate_schedule()

**What:** `Scheduler` takes an `Owner` and a flat `list[Task]`. `generate_schedule()` runs the greedy algorithm: expand → sort → fit.

**When to use:** Phase 3 will call `Scheduler(owner, tasks).generate_schedule()`.

**Example:**
```python
@dataclass
class Scheduler:
    owner: "Owner"
    tasks: list  # list[Task]

    def generate_schedule(self) -> Schedule:
        # Step 1: Expand frequency > 1 tasks into N copies
        expanded = []
        for task in self.tasks:
            for _ in range(task.frequency):
                expanded.append(task)

        # Step 2: Sort by priority (high=0 first)
        sorted_tasks = sorted(expanded, key=lambda t: PRIORITY_ORDER[t.priority])

        # Step 3: Greedy fit — track remaining minutes and running clock
        remaining = self.owner.available_hours * 60
        current = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))
        schedule = Schedule()

        for task in sorted_tasks:
            if task.duration_minutes <= remaining:
                start = current.time()
                current += datetime.timedelta(minutes=task.duration_minutes)
                end = current.time()
                reason = f"Scheduled: priority={task.priority}"
                schedule.blocks.append(TimeBlock(task, start, end, reason))
                remaining -= task.duration_minutes
            else:
                schedule.skipped.append(task)

        return schedule
```

**Note on reason string:** The exact reason wording is Claude's discretion. A minimal reason like `"Scheduled: priority={task.priority}"` satisfies SCHED-04. More descriptive reasons (e.g., `"High-priority task fits within {remaining} min remaining"`) are also valid.

### Pattern 4: datetime.time Arithmetic — The Correct Way

**What:** `datetime.time` does NOT support `+` directly. The correct pattern is to combine with a date into a `datetime.datetime`, add `timedelta`, then extract `.time()`.

**When to use:** Every place you advance the running clock.

**Example:**
```python
import datetime

# WRONG — raises TypeError: unsupported operand type(s)
# new_time = start_time + datetime.timedelta(minutes=30)

# CORRECT — combine, add, extract
base = datetime.datetime.combine(datetime.date.today(), start_time)
end_dt = base + datetime.timedelta(minutes=30)
end_time = end_dt.time()
```

### Pattern 5: Frequency Expansion Before Sort

**What:** Tasks with `frequency=2` must produce TWO `TimeBlock` entries, not one. Expand into a flat list before sorting so the sort treats each occurrence independently.

**When to use:** Always — SCHED-03 is a hard requirement.

**Example:**
```python
# Expand: task with frequency=2 becomes [task, task]
expanded = []
for task in self.tasks:
    for _ in range(task.frequency):
        expanded.append(task)
# Then sort expanded, not self.tasks
sorted_tasks = sorted(expanded, key=lambda t: PRIORITY_ORDER[t.priority])
```

**Pitfall:** If you sort first and expand after, repeated tasks all get identical start times. Always expand BEFORE sort and greedy-fit loop.

### Anti-Patterns to Avoid

- **`datetime.time` + `timedelta` directly:** Raises `TypeError`. Use `datetime.datetime.combine` + `timedelta` + `.time()` pattern.
- **Sorting tasks before frequency expansion:** Each occurrence of a frequency-2 task is independent; expand first so the sort and fit loop sees all occurrences.
- **Tracking time as raw integer minutes:** Loses the ability to display wall-clock times; always track as `datetime.datetime`, display as `.time()`.
- **Defining Scheduler/Schedule/TimeBlock in app.py:** Same as Phase 1 constraint — must be in `models.py` for pytest to import without Streamlit.
- **Modifying the original task objects during scheduling:** The scheduler should not mutate `Task` instances. Expansion creates a new flat list; the originals stay unchanged.
- **Using `tasks * frequency` to expand:** `[task] * n` creates N references to the same object, which is fine for immutable reads but confusing if the scheduler ever needs to annotate occurrences differently (e.g., "occurrence 1 of 2"). An explicit `for _ in range(task.frequency)` loop is cleaner and equally correct.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Time addition across hour boundaries | Manual modulo on integer minutes | `datetime.timedelta` + `datetime.datetime` | `timedelta` handles minute→hour rollover, midnight wrap, and leap seconds automatically |
| Priority comparison | Custom `__lt__` on Task or string comparison | `PRIORITY_ORDER` dict already in `models.py` | Already defined and tested in Phase 1; one line: `key=lambda t: PRIORITY_ORDER[t.priority]` |
| Schedule formatting | Custom template or f-string assembly across multiple methods | Single `explain()` method on Schedule using `strftime` | One method, one place, easy to test |
| Sorting stability concerns | Custom stable sort implementation | Python's `sorted()` is guaranteed stable (Timsort) | Documented Python guarantee: equal-priority tasks preserve insertion order |

**Key insight:** The greedy algorithm is trivially simple once frequency expansion and priority sort are correct. The only real complexity is the `datetime.time` arithmetic trap — everything else is a `sorted()` + `for` loop.

---

## Common Pitfalls

### Pitfall 1: datetime.time Does Not Support Addition

**What goes wrong:** `start_time + datetime.timedelta(minutes=30)` raises `TypeError: unsupported operand type(s) for +: 'datetime.time' and 'datetime.timedelta'`.

**Why it happens:** `datetime.time` represents a clock reading, not a duration. Only `datetime.datetime` and `datetime.timedelta` support arithmetic.

**How to avoid:** Use `datetime.datetime.combine(datetime.date.today(), start_time)` to produce a full datetime, add timedelta, then extract `.time()`. Keep a running `current_dt: datetime.datetime` variable in `generate_schedule()` instead of a `current_time: datetime.time`.

**Warning signs:** `TypeError` in `generate_schedule()` on the first TimeBlock.

### Pitfall 2: Frequency Expansion After Sort

**What goes wrong:** Tasks sorted by priority but expanded after the sort loop assigns all occurrences of a frequency-2 task the same start time, or the second occurrence doesn't advance the clock correctly.

**Why it happens:** If expansion happens inside the greedy loop (e.g., "for each task, schedule it frequency times"), the budget tracking and time advancement logic must repeat — it's easy to double-count or miscalculate remaining minutes.

**How to avoid:** Expand to a flat list first, then sort, then run a single greedy loop over the expanded list. The loop body handles exactly one task occurrence per iteration.

**Warning signs:** A task with `frequency=2` only producing one TimeBlock, or both occurrences having the same start time.

### Pitfall 3: available_hours Stored as Hours, Used as Minutes

**What goes wrong:** `remaining = self.owner.available_hours` sets remaining budget in hours. `task.duration_minutes` is in minutes. The subtraction `remaining -= task.duration_minutes` underflows immediately (e.g., 8 - 30 = -22).

**Why it happens:** Unit mismatch between `Owner.available_hours` (hours) and `Task.duration_minutes` (minutes).

**How to avoid:** Convert at the top of `generate_schedule()`: `remaining = self.owner.available_hours * 60`. All subsequent arithmetic uses minutes.

**Warning signs:** Every task ends up in `schedule.skipped` even when there should be time; or the budget is exhausted after one task.

### Pitfall 4: Mutating tasks list vs. expanding to new list

**What goes wrong:** Appending expanded copies to `self.tasks` in-place causes the Scheduler to accumulate tasks across repeated calls to `generate_schedule()`.

**Why it happens:** `self.tasks` is a shared reference; modifying it changes the underlying list the caller passed in.

**How to avoid:** Always build `expanded = []` as a local variable inside `generate_schedule()`, never mutate `self.tasks`.

**Warning signs:** Second call to `generate_schedule()` produces more TimeBlocks than the first.

### Pitfall 5: Skipped Tasks Silently Dropped

**What goes wrong:** The phase success criterion is "Tasks that exceed the remaining time budget are excluded from the schedule (not silently dropped without record)." If skipped tasks are simply not appended anywhere, the test for skipped tasks cannot pass.

**Why it happens:** It's natural to write `continue` in the greedy loop without an `else` branch.

**How to avoid:** Add `else: schedule.skipped.append(task)` in the greedy loop. Write a pytest test that asserts `len(schedule.skipped) > 0` when tasks exceed the budget.

**Warning signs:** `schedule.skipped` is always empty; skipped-tasks test passes vacuously.

---

## Code Examples

Verified patterns based on stdlib documentation and Phase 1 codebase:

### Complete scheduler classes to add to models.py

```python
# Add to models.py after existing dataclasses
import datetime

@dataclass
class TimeBlock:
    task: "Task"
    start_time: datetime.time
    end_time: datetime.time
    reason: str


@dataclass
class Schedule:
    blocks: list = field(default_factory=list)   # list[TimeBlock]
    skipped: list = field(default_factory=list)  # list[Task]

    def explain(self) -> str:
        if not self.blocks:
            return "No tasks scheduled."
        lines = []
        for block in self.blocks:
            start = block.start_time.strftime("%H:%M")
            end   = block.end_time.strftime("%H:%M")
            lines.append(
                f"{start} - {end}: {block.task.title} "
                f"({block.task.pet.name}) — {block.reason}"
            )
        return "\n".join(lines)


@dataclass
class Scheduler:
    owner: "Owner"
    tasks: list  # list[Task]

    def generate_schedule(self) -> Schedule:
        # Expand frequency > 1 tasks
        expanded = []
        for task in self.tasks:
            for _ in range(task.frequency):
                expanded.append(task)

        # Sort by priority: high(0) → medium(1) → low(2)
        sorted_tasks = sorted(expanded, key=lambda t: PRIORITY_ORDER[t.priority])

        # Greedy fit
        remaining = self.owner.available_hours * 60
        current = datetime.datetime.combine(
            datetime.date.today(), datetime.time(8, 0)
        )
        schedule = Schedule()

        for task in sorted_tasks:
            if task.duration_minutes <= remaining:
                start = current.time()
                current += datetime.timedelta(minutes=task.duration_minutes)
                end = current.time()
                reason = f"Scheduled: priority={task.priority}"
                schedule.blocks.append(TimeBlock(task, start, end, reason))
                remaining -= task.duration_minutes
            else:
                schedule.skipped.append(task)

        return schedule
```

### Test structure for test_scheduler.py

```python
# tests/test_scheduler.py — importable without Streamlit
import models


# -- Fixtures --

def make_owner(hours=2):
    return models.Owner(name="Alex", available_hours=hours)


def make_pet():
    return models.Pet(name="Mochi", species="dog", age=3)


# -- SCHED-01: Scheduler produces a Schedule --

def test_generate_schedule_returns_schedule():
    owner = make_owner(hours=1)
    pet = make_pet()
    tasks = [models.Task("Walk", 20, "high", 1, pet)]
    scheduler = models.Scheduler(owner=owner, tasks=tasks)
    result = scheduler.generate_schedule()
    assert isinstance(result, models.Schedule)


# -- SCHED-02: Priority ordering —-

def test_high_priority_scheduled_before_low():
    owner = make_owner(hours=1)
    pet = make_pet()
    tasks = [
        models.Task("Low task",  10, "low",  1, pet),
        models.Task("High task", 10, "high", 1, pet),
    ]
    scheduler = models.Scheduler(owner=owner, tasks=tasks)
    result = scheduler.generate_schedule()
    titles = [b.task.title for b in result.blocks]
    assert titles.index("High task") < titles.index("Low task")


# -- SCHED-02: Skipped tasks when budget exceeded --

def test_task_exceeding_budget_goes_to_skipped():
    owner = make_owner(hours=0)   # 0 hours = nothing fits
    pet = make_pet()
    tasks = [models.Task("Walk", 30, "high", 1, pet)]
    scheduler = models.Scheduler(owner=owner, tasks=tasks)
    result = scheduler.generate_schedule()
    assert len(result.blocks) == 0
    assert len(result.skipped) == 1


# -- SCHED-03: Frequency expansion --

def test_frequency_2_produces_two_blocks():
    owner = make_owner(hours=2)
    pet = make_pet()
    tasks = [models.Task("Feeding", 10, "high", 2, pet)]
    scheduler = models.Scheduler(owner=owner, tasks=tasks)
    result = scheduler.generate_schedule()
    feeding_blocks = [b for b in result.blocks if b.task.title == "Feeding"]
    assert len(feeding_blocks) == 2


# -- SCHED-04: TimeBlock fields --

def test_timeblock_has_start_end_reason():
    owner = make_owner(hours=1)
    pet = make_pet()
    tasks = [models.Task("Walk", 20, "high", 1, pet)]
    scheduler = models.Scheduler(owner=owner, tasks=tasks)
    result = scheduler.generate_schedule()
    block = result.blocks[0]
    assert hasattr(block, "start_time")
    assert hasattr(block, "end_time")
    assert hasattr(block, "reason")
    assert isinstance(block.reason, str) and len(block.reason) > 0


# -- SCHED-04: end_time > start_time --

def test_timeblock_end_after_start():
    import datetime
    owner = make_owner(hours=1)
    pet = make_pet()
    tasks = [models.Task("Walk", 20, "high", 1, pet)]
    scheduler = models.Scheduler(owner=owner, tasks=tasks)
    result = scheduler.generate_schedule()
    block = result.blocks[0]
    assert block.end_time > block.start_time


# -- SCHED-05: Schedule.explain() --

def test_explain_returns_string():
    owner = make_owner(hours=1)
    pet = make_pet()
    tasks = [models.Task("Walk", 20, "high", 1, pet)]
    scheduler = models.Scheduler(owner=owner, tasks=tasks)
    result = scheduler.generate_schedule()
    explanation = result.explain()
    assert isinstance(explanation, str)
    assert len(explanation) > 0


def test_explain_contains_task_title():
    owner = make_owner(hours=1)
    pet = make_pet()
    tasks = [models.Task("Morning walk", 20, "high", 1, pet)]
    scheduler = models.Scheduler(owner=owner, tasks=tasks)
    result = scheduler.generate_schedule()
    assert "Morning walk" in result.explain()


def test_explain_empty_schedule():
    owner = make_owner(hours=0)
    pet = make_pet()
    tasks = [models.Task("Walk", 30, "high", 1, pet)]
    scheduler = models.Scheduler(owner=owner, tasks=tasks)
    result = scheduler.generate_schedule()
    explanation = result.explain()
    assert isinstance(explanation, str)  # must not crash on empty schedule
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual hour/minute arithmetic in lists | `datetime.timedelta` for time arithmetic | Python 3.3+ | Correct rollover behavior; no modulo bugs |
| Separate "scheduler module" file | All domain classes in one `models.py` | Project decision (Phase 1 context) | Single `import models` in tests; no PYTHONPATH complications |

**Deprecated/outdated:**
- `time.struct_time`: Low-level C struct — use `datetime.time` and `datetime.datetime` instead; cleaner API, supports arithmetic via `timedelta`

---

## Open Questions

1. **Day start time convention**
   - What we know: STATE.md says "datetime.datetime used internally for time arithmetic; convert to .time() for display only" — no specific start time locked
   - What's unclear: Whether the schedule should start at 08:00, 00:00, or be configurable
   - Recommendation: Hard-code `datetime.time(8, 0)` as the start of day in `generate_schedule()`. Phase 3 can expose this as a parameter if needed. 08:00 is a natural "start of day" for pet care.

2. **Reason string content**
   - What we know: SCHED-04 requires a `reason` string — exact content not specified in requirements
   - What's unclear: Whether the reason should explain WHY it was included (e.g., "High-priority task") or just WHAT it is
   - Recommendation: Use `f"Scheduled: priority={task.priority}"` as the minimal viable reason. The planner can choose richer formatting. The key constraint is that the string is non-empty and human-readable.

3. **Multiple pets in tasks list**
   - What we know: `Owner.pets` is a list and tasks reference their pet via `task.pet`; `Scheduler` takes a flat task list
   - What's unclear: Whether Phase 2 tests should cover multi-pet schedules explicitly
   - Recommendation: Write at least one test with tasks from two different pets to confirm `block.task.pet.name` displays correctly in `explain()`.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 9.0.2 |
| Config file | None — pytest discovers `tests/` by convention; no pytest.ini needed |
| Quick run command | `.venv/bin/python -m pytest tests/test_scheduler.py -x` |
| Full suite command | `.venv/bin/python -m pytest tests/ -v` |

Note: Use `.venv/bin/python -m pytest` — bare `pytest` or `python3 -m pytest` resolve to system Python which does not have pytest installed.

### Phase Requirements to Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SCHED-01 | Scheduler(owner, tasks).generate_schedule() returns Schedule instance | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_generate_schedule_returns_schedule -x` | Wave 0 |
| SCHED-02 | High-priority tasks appear before low-priority in blocks | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_high_priority_scheduled_before_low -x` | Wave 0 |
| SCHED-02 | Tasks exceeding budget appear in schedule.skipped | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_task_exceeding_budget_goes_to_skipped -x` | Wave 0 |
| SCHED-03 | Task with frequency=2 produces two TimeBlocks | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_frequency_2_produces_two_blocks -x` | Wave 0 |
| SCHED-04 | TimeBlock has start_time, end_time, reason attributes | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_timeblock_has_start_end_reason -x` | Wave 0 |
| SCHED-04 | end_time is after start_time | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_timeblock_end_after_start -x` | Wave 0 |
| SCHED-05 | Schedule.explain() returns non-empty string | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_explain_returns_string -x` | Wave 0 |
| SCHED-05 | explain() contains task title in output | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_explain_contains_task_title -x` | Wave 0 |
| SCHED-05 | explain() does not crash on empty schedule | unit | `.venv/bin/python -m pytest tests/test_scheduler.py::test_explain_empty_schedule -x` | Wave 0 |
| DEL-01 | Full test suite runs with no Streamlit import | integration | `.venv/bin/python -m pytest tests/ -v` (verify no StreamlitAPIException) | Wave 0 |

### Sampling Rate

- **Per task commit:** `.venv/bin/python -m pytest tests/test_scheduler.py -x`
- **Per wave merge:** `.venv/bin/python -m pytest tests/ -v`
- **Phase gate:** Full suite green (all 8 existing + all new scheduler tests pass) before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/test_scheduler.py` — covers SCHED-01 through SCHED-05 and DEL-01 (all unit tests listed above)
- [ ] `models.py` — add `TimeBlock`, `Schedule`, `Scheduler` classes and `import datetime` at top

*(No new framework install needed — pytest 9.0.2 already installed in .venv)*

---

## Sources

### Primary (HIGH confidence)

- Phase 1 `models.py` (project root) — confirmed `PRIORITY_ORDER`, `Pet`, `Owner`, `Task`, `get_default_tasks` implementation
- Phase 1 `tests/test_models.py` — confirmed 8 tests pass; test file structure to follow
- `.planning/REQUIREMENTS.md` — SCHED-01 through SCHED-05, DEL-01 exact requirement text
- `.planning/ROADMAP.md` — Phase 2 success criteria (5 criteria)
- `.planning/STATE.md` — locked decisions: `datetime.datetime` for arithmetic, `.time()` for display; `PRIORITY_ORDER` dict; `models.py` at project root
- Python stdlib docs: `datetime` module — https://docs.python.org/3/library/datetime.html — `timedelta`, `time`, `datetime.combine`
- Python stdlib docs: `dataclasses` — https://docs.python.org/3/library/dataclasses.html — `field(default_factory=list)`

### Secondary (MEDIUM confidence)

- None required — all technical claims verified against stdlib docs and project files

### Tertiary (LOW confidence)

- None

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — stdlib only; no new libraries; pytest confirmed working at `.venv/bin/python -m pytest`
- Architecture: HIGH — sourced directly from Phase 1 decisions in STATE.md and CONTEXT.md; `models.py` placement locked
- Algorithm: HIGH — greedy scheduler with expand→sort→fit is unambiguous from SCHED-02 and SCHED-03 requirements
- Pitfalls: HIGH — `datetime.time` arithmetic limitation is documented stdlib behavior; unit mismatch is verifiable from models.py; frequency expansion order is derivable from the requirements

**Research date:** 2026-03-20
**Valid until:** 2026-06-20 (stdlib — no change risk; pytest 9.x stable)
