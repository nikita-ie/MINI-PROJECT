import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.file_handler import load_data, save_data

FILE = "data/health.csv"

def show_health_tracker():
    pass

    st.subheader("Health Tracker")

    df = load_data(FILE)

    with st.form("health_form"):

        date = st.date_input("Date")
        water = st.number_input("Water Intake (Litres)", min_value=0.0)
        sleep = st.number_input("Sleep Hours", min_value=0.0)
        medicine = st.text_input("Medicine Reminder")

        submit = st.form_submit_button("Save Health Data")

        if submit:

            new_data = {
                "Date": [date],
                "Water Intake": [water],
                "Sleep Hours": [sleep],
                "Medicine Reminder": [medicine]
            }

            new_df = pd.DataFrame(new_data)

            df = pd.concat([df, new_df], ignore_index=True)

            save_data(df, FILE)

            st.success("Health Data Saved")

    st.write("Daily Health Summary")
    st.dataframe(df)

    if not df.empty:

        fig, ax = plt.subplots()

        ax.plot(df["Water Intake"])

        ax.set_title("Water Intake Progress")

        st.pyplot(fig)