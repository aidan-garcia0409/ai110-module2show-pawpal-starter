# models.py — pure Python, importable without Streamlit
from dataclasses import dataclass, field

# Numeric sort keys — prevents alphabetical priority comparison bug
# Phase 2 scheduler uses: sorted(tasks, key=lambda t: PRIORITY_ORDER[t.priority])
PRIORITY_ORDER: dict[str, int] = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Pet:
    name: str
    species: str        # "dog" | "cat"
    age: int
    preferences: dict = field(default_factory=dict)


@dataclass
class Owner:
    name: str
    available_hours: int
    pets: list = field(default_factory=list)


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str       # "high" | "medium" | "low"
    frequency: int = 1  # times per day
    pet: "Pet | None" = None


def get_default_tasks(pet: Pet) -> list:
    """Return pre-constructed Task objects for the given pet's species.

    Args:
        pet: A Pet object whose species determines the returned task list.

    Returns:
        List of Task objects pre-assigned to the given pet.

    Raises:
        ValueError: If pet.species is not "dog" or "cat".
    """
    if pet.species == "dog":
        return [
            Task("Morning walk",  30, "high",   1, pet),
            Task("Feeding",       10, "high",   2, pet),
            Task("Water refresh",  5, "medium", 2, pet),
            Task("Evening walk",  30, "high",   1, pet),
            Task("Playtime",      20, "medium", 1, pet),
            Task("Grooming",      15, "low",    1, pet),
        ]
    elif pet.species == "cat":
        return [
            Task("Feeding",       10, "high",   2, pet),
            Task("Water refresh",  5, "medium", 2, pet),
            Task("Litter box",    10, "high",   1, pet),
            Task("Playtime",      15, "medium", 1, pet),
            Task("Brushing",      10, "low",    1, pet),
            Task("Nail trim",      5, "low",    1, pet),
        ]
    else:
        raise ValueError(f"No default tasks for species: {pet.species!r}")
