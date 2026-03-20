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
