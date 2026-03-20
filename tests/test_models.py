# tests/test_models.py — importable without Streamlit
import models


def test_pet_importable_without_streamlit():
    pet = models.Pet(name="Mochi", species="dog", age=3)
    assert pet.name == "Mochi"
    assert pet.preferences == {}


def test_owner_fields():
    owner = models.Owner(name="Alex", available_hours=8)
    assert owner.name == "Alex"
    assert owner.available_hours == 8
    assert owner.pets == []


def test_task_fields():
    pet = models.Pet("Rex", "dog", 2)
    task = models.Task(title="Walk", duration_minutes=30, priority="high", pet=pet)
    assert task.title == "Walk"
    assert task.duration_minutes == 30
    assert task.priority == "high"
    assert task.frequency == 1  # default
    assert task.pet is pet


def test_priority_order_correct():
    assert models.PRIORITY_ORDER["high"] < models.PRIORITY_ORDER["medium"]
    assert models.PRIORITY_ORDER["medium"] < models.PRIORITY_ORDER["low"]


def test_get_default_tasks_dog_returns_tasks():
    pet = models.Pet("Rex", "dog", 2)
    tasks = models.get_default_tasks(pet)
    assert len(tasks) >= 6
    assert all(isinstance(t, models.Task) for t in tasks)
    assert all(t.pet is pet for t in tasks)


def test_get_default_tasks_dog_has_frequency_gt_1():
    pet = models.Pet("Rex", "dog", 2)
    tasks = models.get_default_tasks(pet)
    assert any(t.frequency > 1 for t in tasks)


def test_get_default_tasks_cat_returns_tasks():
    pet = models.Pet("Luna", "cat", 1)
    tasks = models.get_default_tasks(pet)
    assert len(tasks) >= 6
    assert all(isinstance(t, models.Task) for t in tasks)
    assert all(t.pet is pet for t in tasks)


def test_get_default_tasks_unknown_species_raises():
    pet = models.Pet("Buddy", "other", 4)
    try:
        models.get_default_tasks(pet)
        assert False, "Expected ValueError"
    except ValueError:
        pass
