# Code Conventions

## Language & Style

- **Language:** Python 3
- **Style:** PEP 8 (implicit — no linter/formatter configured)
- **No type hints** in existing code (starter is intentionally minimal)
- **No docstrings** in existing code (students expected to add their own)

## Naming

| Element | Convention | Example |
|---|---|---|
| Variables | snake_case | `owner_name`, `task_title`, `duration_minutes` |
| Functions | snake_case | (none defined yet) |
| Classes | PascalCase | (expected by project: `Pet`, `Owner`, `Task`) |
| Constants | UPPER_SNAKE_CASE | (none defined yet) |

## Streamlit Patterns

### Session State
```python
if "tasks" not in st.session_state:
    st.session_state.tasks = []
```
Use guard pattern before accessing `st.session_state` keys.

### Layout
- `st.columns()` for horizontal layouts
- `st.expander()` for collapsible sections
- `st.divider()` to separate sections

### Input Widgets
- `st.text_input()` for strings
- `st.number_input()` for numeric values with `min_value`/`max_value`
- `st.selectbox()` for enums/choices

### Feedback
- `st.warning()` for unimplemented features
- `st.info()` for empty states
- `st.table()` for tabular data

## Data Structures

Task dictionary shape (from `st.session_state.tasks`):
```python
{
    "title": str,
    "duration_minutes": int,
    "priority": "low" | "medium" | "high"
}
```

## File Organization

- **Single file** (`app.py`) — all UI code lives here for the starter
- **Expected expansion:** Students should create separate modules for domain logic (e.g., `scheduler.py`, `models.py`) and import into `app.py`

## Error Handling

- No error handling in starter code
- `st.warning()` used as placeholder for unimplemented logic
- Students expected to add validation as part of implementation

## Configuration

- No `.env` or config files present
- `st.set_page_config()` used for app-level Streamlit config at top of `app.py`
