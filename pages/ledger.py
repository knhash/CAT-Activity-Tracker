# ledger.py
from datetime import datetime
import pandas as pd
import streamlit as st
from data import load_ledger_data, save_ledger_data

def ledger():  
    # st.title("Cat Management :orange[Ledger]")  
  
    # Input form  
    with st.form("ledger_form"):  
        category = st.selectbox("Category", ["Food", "Medical", "Service", "Extra"])  
        description = st.text_input("Description")  
        amount = st.number_input("Amount", min_value=0.0, step=1.0)  
        date = st.date_input("Date", value=datetime.now().date())  

        submit_button = st.form_submit_button("Add Expense")  

    if submit_button:  
        new_expense = pd.DataFrame([[description, category, amount, date]], columns=["Description", "Category", "Amount", "Date"])  
        ledger_data = load_ledger_data()  
        ledger_data = pd.concat([ledger_data, new_expense], ignore_index=True)
        save_ledger_data(ledger_data)  
  
    # Display ledger data  
    ledger_data = load_ledger_data()  
    st.subheader("All transactions", divider="rainbow")  
    st.dataframe(ledger_data, use_container_width=True, hide_index=True)  