# Technology Stack

**Project:** PawPal — Python OOP Scheduling App with Streamlit UI
**Researched:** 2026-03-19

---

## Recommended Stack

### Core Framework

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Python | 3.11+ | Runtime | dataclasses and `datetime.time` work correctly; widely installed in school environments |
| Streamlit | >=1.30 (project floor) | UI layer | Assignment-mandated. Handles session state, widget loop, and display. No JavaScript required. |
| pytest | >=7.0 (project floor) | Unit testing | Assignment-mandated. Standard Python test runner. Simple function-based tests with no boilerplate. |

---

### Standard Library (No Extra Dependencies)

| Module | Purpose | Why |
|--------|---------|-----|
| `datetime` (`time`, `timedelta`) | TimeBlock start/end times | Built-in. `datetime.time` is the correct type for a daily schedule. |
| `dataclasses` | `@dataclass` for models | Built-in since Python 3.7. Eliminates `__init__` boilerplate for Pet, Task, TimeBlock, Schedule. Pure data — easy to test. |
| `enum` | Priority enum | Built-in. `Priority(str, Enum)` with values `"low"/"medium"/"high"` gives ordering + Streamlit selectbox compatibility. |

---

### UML Diagramming

| Tool | Purpose | Why |
|------|---------|-----|
| Mermaid (inline in Markdown) | Class diagram for submission | Zero install, renders in GitHub README and VS Code. `classDiagram` directive maps directly to Owner/Pet/Task/Scheduler/Schedule/TimeBlock. |

**Rejected:** PlantUML (requires Java), pyreverse (binary output), draw.io (not version-control friendly).

---

## Module Structure for Testability

```
pawpal/
    __init__.py
    models.py        # Pet, Owner, Task — pure dataclasses, NO Streamlit imports
    scheduler.py     # Scheduler, Schedule, TimeBlock — pure logic, NO Streamlit imports
    defaults.py      # Default task library per species — pure data, NO Streamlit imports
app.py               # ONLY Streamlit code — imports from pawpal/, never contains logic
tests/
    __init__.py
    test_models.py
    test_scheduler.py
```

**Critical rule:** `models.py` and `scheduler.py` must have zero Streamlit imports. pytest can then import and test them directly without a running Streamlit server.

**Anti-pattern to avoid:** Defining `Pet` or `Scheduler` inside `app.py`. This makes all pytest tests require Streamlit to be imported — the single most common mistake in Streamlit school projects.

---

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| UI | Streamlit | Flask | Assignment specifies Streamlit |
| Testing | pytest | unittest | pytest has simpler syntax; already pinned in requirements.txt |
| Data models | `@dataclass` | Pydantic | Overkill for session-state-only app; adds dependency |
| UML | Mermaid | PlantUML | PlantUML requires Java runtime |

---

## Installation

```bash
pip install "streamlit>=1.30"
pip install "pytest>=7.0"
# Optional coverage:
pip install "pytest-cov>=4.0"
```

No other installs required. All other components are Python stdlib.
