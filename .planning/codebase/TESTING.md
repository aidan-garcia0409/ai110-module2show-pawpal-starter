# Testing

## Framework

- **pytest** listed as dependency (`requirements.txt`: `pytest>=7.0`)
- No test files exist yet (starter template — students add tests)
- No `pytest.ini`, `conftest.py`, or `setup.cfg` configured

## Current State

**No tests exist.** This is an intentional starter scaffold.

The project expects students to write tests for their scheduling/domain logic as part of the implementation exercise.

## Expected Test Structure

Based on project requirements, tests should cover:

```
tests/
├── test_models.py       # Pet, Owner, Task classes
├── test_scheduler.py    # Scheduling logic and constraints
└── conftest.py          # Shared fixtures (optional)
```

## Running Tests

```bash
pytest
# or
python -m pytest -v
```

## What to Test

Per the project brief, students should test:
- Task representation (title, duration, priority)
- Pet/Owner model behavior
- Scheduling logic (task selection, ordering, constraints)
- Plan explanation output

## Patterns to Follow

### Unit test structure (pytest)
```python
def test_task_has_required_fields():
    task = Task(title="Morning walk", duration_minutes=20, priority="high")
    assert task.title == "Morning walk"
    assert task.duration_minutes == 20
    assert task.priority == "high"
```

### Fixture pattern
```python
import pytest

@pytest.fixture
def sample_pet():
    return Pet(name="Mochi", species="dog")

def test_scheduler_with_pet(sample_pet):
    scheduler = Scheduler(pet=sample_pet)
    # ...
```

## Streamlit Testing

- Streamlit UI (`app.py`) is **not unit-testable** without additional tooling
- Focus tests on pure Python domain logic (models, scheduler)
- UI correctness validated manually via the running app

## Coverage

- No coverage tooling configured
- Students may add `pytest-cov` if desired: `pip install pytest-cov`
- Run with: `pytest --cov=. --cov-report=term-missing`
