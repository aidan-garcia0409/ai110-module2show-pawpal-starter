# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Class Diagram

The diagram below shows all six domain classes and their relationships.

```mermaid
classDiagram
    class Owner {
        str name
        int available_hours
        list~Pet~ pets
    }
    class Pet {
        str name
        str species
        int age
        dict preferences
    }
    class Task {
        str title
        int duration_minutes
        str priority
        int frequency
        Pet pet
    }
    class Scheduler {
        Owner owner
        list~Task~ tasks
        generate_schedule() Schedule
    }
    class Schedule {
        list~TimeBlock~ blocks
        explain() str
    }
    class TimeBlock {
        Task task
        time start_time
        time end_time
        str reason
    }
    Owner "1" *-- "many" Pet : has
    Pet "1" *-- "many" Task : assigned to
    Scheduler --> Owner : uses
    Scheduler --> Schedule : produces
    Schedule "1" *-- "many" TimeBlock : contains
    TimeBlock --> Task : references
```
