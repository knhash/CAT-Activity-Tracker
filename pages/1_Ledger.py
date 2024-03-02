# ledger.py
from datetime import datetime
import pandas as pd
import streamlit as st
from data import load_ledger_data, save_ledger_data
from sidebar import gen_sidebar

# Define a function to highlight alternate months

def ledger():  
    # st.title("Cat Management :orange[Ledger]")  
  
    # Input form  
    with st.form("ledger_form"):  
        category = st.selectbox("Category", ["Food", "Vet", "Misc"])  
        description = st.text_input("Description")  
        amount = st.number_input("Amount", min_value=0.0, step=1.0)  
        date = st.date_input("Date", value=datetime.now().date())  

        submit_button = st.form_submit_button("Add Expense")  

    if submit_button:  
        new_expense = pd.DataFrame([[description, category, amount, date]], columns=["Description", "Category", "Amount", "Date"])  
        ledger_data = load_ledger_data()  
        ledger_data = pd.concat([ledger_data, new_expense], ignore_index=True)
        save_ledger_data(ledger_data)  
  
    ledger_data = load_ledger_data()  
    
    # Average monthly expenses grouped by category
    st.subheader("Average monthly expenses", divider="rainbow")
    ledger_data['Datetime'] = pd.to_datetime(ledger_data['Date'])
    monthly_expenses = ledger_data.groupby([ledger_data.Datetime.dt.month, "Category"]).Amount.sum().unstack().fillna(0)
    # monthly_expenses = monthly_expenses.applymap(lambda x: f"₹{x:,.0f}")
    # Calculate the average of averages
    average_expenses = monthly_expenses.mean()
    sum_of_amounts = average_expenses.sum()
    # average_expenses = average_expenses.apply(lambda x: f"₹{x:,.0f}")
    # Calculate the sum of the amounts for each category
    # st.write(average_expenses.to_dict(), sum_of_amounts)

    cols = st.columns(3)
    index = 0
    for key, value in average_expenses.to_dict().items():
        with cols[index]:
            st.metric(
                key,
                "₹{:,.2f}".format(value),
                delta = "{:,.2f}%".format(float(value)/sum_of_amounts*100),
                delta_color="off"
            )
        index += 1



    # st.dataframe(average_expenses, use_container_width=True)



    # All transactions
    st.subheader("All transactions", divider="rainbow")  
    # ledger_data['Amount'] = ledger_data['Amount'].apply(lambda x: "₹{:,.0f}".format(x))
    # st.dataframe(
    #     ledger_data, 
    #     use_container_width=True, 
    #     hide_index=True,
    #     column_order=("Date", "Category", "Description", "Amount")
    #     )  
    ledger_data_edited = st.data_editor(
        ledger_data, 
        use_container_width=True, 
        hide_index=True,
        column_order=("Date", "Category", "Amount", "Description"),
        num_rows="dynamic",
        disabled=("Date", "Category", "Amount", "Description"),
    )
    if ledger_data_edited is not None:
        save_ledger_data(ledger_data_edited)

def main():

    _=st.set_page_config(
        page_title="CAT Activity Tracker",
        page_icon="🐈",
        initial_sidebar_state="collapsed",
        layout="centered",
        ),

    st.title(f"Cat Management :orange[Ledger]")

    ledger()

    with st.sidebar:
        gen_sidebar()
        
if __name__ == "__main__":
    main()