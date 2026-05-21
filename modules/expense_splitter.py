import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.file_handler import load_data, save_data

FILE = "data/expenses.csv"

def show_expense_splitter():

    st.subheader("Mess & Food Expense Splitter")

    df = load_data(FILE)

    with st.form("expense_form"):

        date = st.date_input("Date")
        title = st.text_input("Expense Title")
        amount = st.number_input("Amount", min_value=0.0)
        paid_by = st.text_input("Paid By")
        split_among = st.text_input("Split Among")

        submit = st.form_submit_button("Add Expense")

        if submit:

            new_data = {
                "Date": [date],
                "Title": [title],
                "Amount": [amount],
                "Paid By": [paid_by],
                "Split Among": [split_among]
            }

            new_df = pd.DataFrame(new_data)

            df = pd.concat([df, new_df], ignore_index=True)

            save_data(df, FILE)

            st.success("Expense Added")

    st.write("Expense History")
    st.dataframe(df)

    if not df.empty:

        total = df["Amount"].sum()

        st.metric("Total Expenses", f"₹ {total}")

        person_expense = df.groupby("Paid By")["Amount"].sum()

        fig, ax = plt.subplots()

        ax.pie(
            person_expense,
            labels=person_expense.index,
            autopct='%1.1f%%'
        )

        st.pyplot(fig)