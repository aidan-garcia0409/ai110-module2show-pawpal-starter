# Codebase Concerns

## Summary

This is an intentional starter scaffold — most "concerns" are by design (students implement the missing pieces). However, there are structural gaps and quality issues to be aware of when building on top of this.

---

## Critical: Missing Implementation (By Design)

These are expected gaps — the starter is a thin scaffold:

| Gap | Location | Notes |
|---|---|---|
| No scheduling logic | `app.py:74` | Core feature stub — `st.warning("Not implemented yet")` |
| No domain models | — | `Pet`, `Owner`, `Task`, `Schedule` classes don't exist yet |
| No data persistence | — | Only Streamlit `session_state` (lost on page refresh) |
| No unit tests | — | `pytest` in requirements but zero test files |

---

## Code Quality Concerns

### No Input Validation
- `app.py` collects user input (owner name, pet name, task title) with no sanitization
- `st.number_input` provides basic bounds (`min_value=1, max_value=240`) but no semantic validation
- No validation for empty strings in text inputs

### No Error Handling
- No `try/except` blocks anywhere
- No graceful degradation if scheduling logic raises exceptions
- Users would see raw Python tracebacks

### No Type Hints or Docstrings
- `app.py` has no type annotations
- No module-level or function-level documentation
- Students should add these as they implement domain classes

### Fragile Session State
- `st.session_state.tasks` is a plain list of dicts — no schema enforcement
- Streamlit reruns the entire script on every interaction; state can diverge if not carefully managed
- No mechanism to clear/reset tasks

---

## Dependency Concerns

### Unpinned Dependencies
`requirements.txt` uses `>=` version constraints:
```
streamlit>=1.30
pytest>=7.0
```
- Risk: future breaking changes in Streamlit could silently break the app
- Recommendation: pin to exact versions (`streamlit==1.32.0`) for reproducibility

### No Lock File
- No `pip freeze` output or `requirements.lock`
- Different environments may install different versions

---

## Security Concerns

### No Authentication
- App has no login or access control
- Acceptable for a local student project; not suitable for deployment

### No Input Sanitization
- Text inputs are rendered directly via `st.table()` and `st.markdown()`
- Streamlit escapes HTML in most contexts, but worth being explicit if rendering user content in markdown

### No Secrets Management
- No `.env` file or secret keys currently
- If students add external APIs (e.g., OpenAI), they should use `st.secrets` or environment variables — not hardcode keys

---

## Architecture Concerns

### Single-File App
- All UI code in `app.py` — will become unwieldy as features are added
- Recommended: extract domain logic to separate modules (`models.py`, `scheduler.py`) and import into `app.py`

### No Separation of Concerns
- UI and data logic are interleaved in `app.py`
- The task dict structure (`{"title": str, "duration_minutes": int, "priority": str}`) is defined implicitly, not enforced

### No Schedule Output UI
- "Generate schedule" button exists but produces no output
- Students need to add schedule display UI (results, explanations) as they implement logic

---

## Testing Concerns

### Zero Test Coverage
- No tests exist despite pytest being a dependency
- No `conftest.py`, no fixtures, no test directory
- Students must establish test patterns from scratch

### Streamlit Untestable via Unit Tests
- `app.py` UI logic cannot be unit tested without `streamlit.testing` or mocking
- Domain logic (models, scheduler) should be kept separate for testability

---

## Technical Debt Tracker

| Item | Priority | Effort | Notes |
|---|---|---|---|
| Add domain models (Pet, Owner, Task) | High | Medium | Required for any scheduling logic |
| Implement scheduling algorithm | High | High | Core project requirement |
| Add unit tests | High | Medium | Required by project spec |
| Pin dependency versions | Low | Low | `requirements.txt` pinning |
| Add input validation | Medium | Low | Empty string guards, etc. |
| Extract logic to modules | Medium | Low | `models.py`, `scheduler.py` |
| Add schedule output UI | Medium | Medium | Display results + explanations |
