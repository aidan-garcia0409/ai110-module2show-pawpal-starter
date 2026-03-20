# Codebase Structure

**Analysis Date:** 2026-03-19

## Directory Layout

```
pawpal-starter/
├── app.py                    # Streamlit UI entry point
├── requirements.txt          # Python dependencies
├── README.md                 # Project overview and setup instructions
├── reflection.md             # Project reflection template (to be filled)
├── .gitignore               # Git ignore rules
└── .planning/
    └── codebase/            # Architecture documentation directory
        ├── ARCHITECTURE.md  # System design patterns and layers
        └── STRUCTURE.md     # This file - directory organization
```

## Directory Purposes

**Project Root:**
- Purpose: Main application and project files
- Contains: Streamlit app, configuration, documentation

**.planning/codebase/:**
- Purpose: Architecture and design documentation
- Contains: ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md, TESTING.md, etc.
- Status: Managed by `/gsd:map-codebase` command

## Key File Locations

**Entry Points:**
- `app.py`: Main Streamlit application - serves the web UI on port 8501

**Configuration:**
- `requirements.txt`: Python package dependencies (streamlit, pytest)
- `.gitignore`: Specifies files to exclude from version control

**Documentation:**
- `README.md`: Project scenario, requirements, and setup instructions
- `reflection.md`: Template for project reflection (UML design, logic, testing, AI usage)

**Testing (To Be Created):**
- Suggested location: `tests/` directory with `test_*.py` files
- Suggested pattern: One test file per module (e.g., `test_scheduler.py`)

**Core Logic (To Be Created):**
- Suggested location: `pawpal/` or similar package directory
- Suggested structure:
  - `pawpal/models.py` - Pet, Owner, Task, Schedule classes
  - `pawpal/scheduler.py` - Scheduling algorithm
  - `pawpal/__init__.py` - Package initialization

## Naming Conventions

**Files:**
- Entry point: `app.py` (main Streamlit application)
- Test files: `test_*.py` (follows pytest convention)
- Core modules: `lowercase_with_underscores.py`
- Documentation: `UPPERCASE.md` (for generated docs) or `lowercase.md` (for user-facing docs)

**Directories:**
- Source package: `pawpal/` or similar business domain name
- Tests: `tests/` (separate from source)
- Documentation: `docs/` or `.planning/` (for architecture docs)

**Classes and Functions:**
- Classes: PascalCase (e.g., `Pet`, `Scheduler`, `Schedule`)
- Functions: snake_case (e.g., `generate_schedule()`, `validate_task()`)
- Constants: UPPER_SNAKE_CASE

**Variables:**
- Local variables: snake_case
- Session state keys: snake_case (e.g., `st.session_state.tasks`)

## Where to Add New Code

**New Business Logic Classes:**
- Primary code: Create `pawpal/models.py` for Pet, Owner, Task, Schedule classes
- Tests: Create `tests/test_models.py` for model tests

**Scheduling Algorithm:**
- Implementation: Create `pawpal/scheduler.py` with Scheduler class
- Tests: Create `tests/test_scheduler.py` for scheduling logic tests
- Integration: Import and call in `app.py` when "Generate schedule" button is clicked

**UI Components:**
- Streamlit UI code: Add to `app.py` or break into functions within `app.py`
- Avoid creating separate Streamlit page files unless adding multi-page features

**Utilities and Helpers:**
- Shared validation: `pawpal/validation.py`
- Shared formatting: `pawpal/formatting.py`
- Or keep in respective modules if tightly coupled

## Special Directories

**.venv/**
- Purpose: Python virtual environment
- Generated: Yes (by `python -m venv .venv`)
- Committed: No (excluded by .gitignore)

**.git/**
- Purpose: Git version control metadata
- Generated: Yes (by `git init`)
- Committed: No (git internals)

**__pycache__/**
- Purpose: Python bytecode cache
- Generated: Yes (automatic by Python)
- Committed: No (excluded by .gitignore)

**.planning/codebase/**
- Purpose: Generated architecture documentation
- Generated: Yes (by `/gsd:map-codebase`)
- Committed: Yes (part of project documentation)

## Project Setup and Execution

**Development Environment:**
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

**Running Tests (Once Created):**
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_scheduler.py
```

---

*Structure analysis: 2026-03-19*
