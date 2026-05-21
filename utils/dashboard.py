import streamlit as st
import pandas as pd

def show_dashboard(expenses, health, assignments):

    st.markdown("## Upcoming Tasks & Reminders")

    reminders = []

    # Expense reminders
    if not expenses.empty:

        for i in range(len(expenses)):

            reminders.append(
                {
                    "task": f"Mess payment pending by {expenses.iloc[i]['Paid By']}",
                    "type": "Expense"
                }
            )

    # Health reminders
    if not health.empty:

        for i in range(len(health)):

            medicine = health.iloc[i]["Medicine Reminder"]

            if str(medicine) != "nan" and medicine != "":

                reminders.append(
                    {
                        "task": f"Take medicine: {medicine}",
                        "type": "Health"
                    }
                )

    # Assignment reminders
    if not assignments.empty:

        pending = assignments[
            assignments["Status"] == "Pending"
        ]

        for i in range(len(pending)):

            reminders.append(
                {
                    "task": f"Submit {pending.iloc[i]['Assignment']}",
                    "type": "Assignment"
                }
            )

    # Session state for deleting reminders
    if "removed_tasks" not in st.session_state:
        st.session_state.removed_tasks = []

    # CENTER SECTION
    left, center, right = st.columns([1,2,1])

    with center:

        st.subheader("To-Do List")

        if len(reminders) == 0:
            st.info("No reminders available")

        for index, reminder in enumerate(reminders):

            task = reminder["task"]

            if task not in st.session_state.removed_tasks:

                col1, col2 = st.columns([5,1])

                with col1:
                    st.checkbox(task, key=f"task_{index}")

                with col2:

                    if st.button("❌", key=f"remove_{index}"):

                        st.session_state.removed_tasks.append(task)

                        st.rerun()