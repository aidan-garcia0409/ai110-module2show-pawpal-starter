import streamlit as st
from models import Pet, Owner, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

AVAILABLE_HOURS = 8  # default time budget; no UI field in v1 (UX-01 deferred to v2)

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        pet = Pet(name=pet_name, species=species, age=0)
        owner = Owner(name=owner_name, available_hours=AVAILABLE_HOURS)
        tasks = [
            Task(
                title=t["title"],
                duration_minutes=t["duration_minutes"],
                priority=t["priority"],
                frequency=1,   # UI does not collect frequency; KeyError if read from dict
                pet=pet,
            )
            for t in st.session_state.tasks
        ]
        st.session_state.schedule = Scheduler(owner=owner, tasks=tasks).generate_schedule()

if "schedule" in st.session_state:
    schedule = st.session_state.schedule
    if not schedule.blocks:
        st.warning("No tasks fit the time budget. Try adding shorter or higher-priority tasks.")
    else:
        st.subheader("Today's Schedule")
        st.table([
            {
                "Start": b.start_time.strftime("%H:%M"),
                "Task": b.task.title,
                "Pet": b.task.pet.name,
                "Reason": b.reason,
            }
            for b in schedule.blocks
        ])

    if schedule.skipped:
        st.subheader("Skipped Tasks")
        st.table([
            {"Task": t.title, "Duration (min)": t.duration_minutes, "Priority": t.priority}
            for t in schedule.skipped
        ])
