import streamlit as st
import pandas as pd
from utils.file_handler import load_data, save_data

FILE = "data/assignments.csv"
def show_assignment_reminder():

    st.subheader("Assignment Reminder")

    df = load_data(FILE)

    with st.form("assignment_form"):

        subject = st.text_input("Subject")
        assignment = st.text_input("Assignment")
        due_date = st.date_input("Due Date")

        priority = st.selectbox(
            "Priority",
            ["High", "Medium", "Low"]
        )

        status = st.selectbox(
            "Status",
            ["Pending", "Completed"]
        )

        submit = st.form_submit_button("Add Assignment")

        if submit:

            new_data = {
                "Subject": [subject],
                "Assignment": [assignment],
                "Due Date": [due_date],
                "Priority": [priority],
                "Status": [status]
            }

            new_df = pd.DataFrame(new_data)

            df = pd.concat([df, new_df], ignore_index=True)

            save_data(df, FILE)

            st.success("Assignment Added")

    st.write("Assignments")
    st.dataframe(df)

    pending = df[df["Status"] == "Pending"]

    st.write("Pending Assignments")

    st.dataframe(pending)