# Architecture

**Analysis Date:** 2026-03-19

## Pattern Overview

**Overall:** Starter/Template Architecture (To Be Implemented)

**Key Characteristics:**
- Thin presentation layer (Streamlit UI) with minimal business logic
- Session-based state management for UI interactions
- Placeholder structure awaiting core scheduling system implementation
- Designed for iterative development starting with UML design

## Layers

**Presentation Layer (UI):**
- Purpose: Interactive interface for user input and schedule display
- Location: `app.py`
- Contains: Streamlit page configuration, input controls, session state management
- Depends on: Streamlit framework, Python standard library
- Used by: End users accessing the web interface

**Business Logic Layer (To Be Implemented):**
- Purpose: Core scheduling algorithm and domain entities (Pet, Owner, Task, Schedule)
- Location: To be created during project implementation
- Contains: Classes for Pet, Owner, Task, scheduling logic
- Depends on: Domain models and business rules
- Used by: Presentation layer and test suite

**Data Layer (To Be Implemented):**
- Purpose: Storage and retrieval of pet, owner, and task information
- Location: To be created during project implementation
- Contains: Data models, persistence logic
- Depends on: Business logic layer
- Used by: Business logic layer

## Data Flow

**User Input Flow:**

1. User enters owner name, pet name, and species through UI input fields
2. User adds tasks via form inputs (title, duration, priority)
3. Tasks are stored in `st.session_state.tasks` (in-memory state)
4. User clicks "Generate schedule" button

**Schedule Generation Flow (To Be Implemented):**

1. Scheduler receives owner, pet, and task list
2. Scheduler applies constraints (time, priority, preferences)
3. Scheduler produces ordered plan with explanations
4. Results are displayed in UI

**State Management:**
- Current: Streamlit session state stores task list in memory (`st.session_state.tasks`)
- Future: Should include Pet, Owner, and generated Schedule objects in session state

## Key Abstractions

**Task (To Be Implemented):**
- Purpose: Represents a pet care activity with metadata
- Examples: Morning walk, feeding, medication, enrichment
- Pattern: Likely value object with attributes (title, duration_minutes, priority)

**Pet (To Be Implemented):**
- Purpose: Represents the animal being cared for
- Pattern: Domain entity with attributes (name, species, preferences)

**Owner (To Be Implemented):**
- Purpose: Represents the human responsible for care
- Pattern: Domain entity with attributes (name, preferences, constraints)

**Scheduler (To Be Implemented):**
- Purpose: Algorithm that builds daily plan from tasks and constraints
- Pattern: Service/algorithm class that takes inputs and produces schedule
- Responsibilities: Task ordering, constraint satisfaction, plan explanation

**Schedule (To Be Implemented):**
- Purpose: Represents the output - ordered list of tasks with reasoning
- Pattern: Value object containing task sequence and decision explanations

## Entry Points

**Web Application:**
- Location: `app.py`
- Triggers: User navigates to Streamlit app URL
- Responsibilities:
  - Render UI
  - Collect owner/pet/task information
  - Call scheduler when user requests
  - Display results
  - Manage session state

## Error Handling

**Strategy:** To be determined during implementation

**Current Pattern:**
- UI shows warning message when "Generate schedule" is clicked (feature not yet implemented)
- No error handling for invalid inputs

## Cross-Cutting Concerns

**Logging:** Not yet implemented

**Validation:** Basic Streamlit input validation (number ranges, selectbox options)

**Authentication:** Not applicable for starter project

---

*Architecture analysis: 2026-03-19*
