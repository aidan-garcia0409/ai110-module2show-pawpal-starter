# Technology Stack

**Analysis Date:** 2026-03-19

## Languages

**Primary:**
- Python 3.14.3 - Core application development and scheduling logic

**Secondary:**
- Markdown - Documentation and project notes

## Runtime

**Environment:**
- Python 3.14.3
- Virtual environment at `.venv/`

**Package Manager:**
- pip 26.0
- Lockfile: `requirements.txt` (minimal - only top-level dependencies specified)

## Frameworks

**Core:**
- Streamlit 1.55.0 - Interactive web UI for pet care planning assistant

**Testing:**
- pytest 9.0.2 - Unit and integration test framework

**Build/Dev:**
- No build tool configured (pure Python application)

## Key Dependencies

**Critical:**
- Streamlit 1.55.0 - Why it matters: Primary UI framework for the interactive pet care planner application. Provides session state management, input widgets, and data display components.

**Data/Utilities:**
- pandas 2.3.3 - Data manipulation and analysis, used for handling task data and schedules
- numpy 2.4.3 - Numerical computing support
- Pillow 12.1.1 - Image processing capabilities

**Data Visualization:**
- altair 6.0.0 - Declarative visualization library
- pyarrow 23.0.1 - Apache Arrow support for efficient data handling
- pydeck 0.9.1 - Deck.gl visualization wrapper

**Utilities:**
- GitPython 3.1.46 - Git repository interaction
- requests 2.32.5 - HTTP client library
- python-dateutil 2.9.0.post0 - Date and time utilities
- pytz 2026.1.post1 - Timezone support
- toml 0.10.2 - TOML parser for configuration files

**Testing Support:**
- pytest 9.0.2 - Test runner and assertion library

## Configuration

**Environment:**
- Configuration via Python code in `app.py`
- Streamlit page config: `st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")`
- No environment variables currently configured

**Build:**
- No build configuration files (poetry.lock, setup.py, pyproject.toml)
- Direct pip-based dependency management

## Platform Requirements

**Development:**
- Python 3.14.3
- Virtual environment (`.venv/`)
- Standard Python tooling (pip)
- macOS, Linux, or Windows with Python 3.14+

**Production:**
- Python 3.14.3 runtime
- Streamlit deployment compatible (runs as web application)
- Can be deployed to Streamlit Cloud, Docker containers, or traditional Python hosting

---

*Stack analysis: 2026-03-19*
