# ledger.py
from datetime import datetime
import pandas as pd
import streamlit as st
from data import load_ledger_data, save_ledger_data
from sidebar import gen_sidebar

# Define a function to highlight alternate months
def highlight_alternate_months(data):
    attr = 'background-color: {}'
    color = 'pink'
    other_color = ''
    is_highlight = False
    month = None
    output = pd.DataFrame(attr.format(other_color), index=data.index, columns=data.columns)
    for index, row in data.iterrows():
        date = row['Date']
        if month is None or date.month != month:
            is_highlight = not is_highlight
            month = date.month
        if is_highlight:
            output.loc[index, :] = attr.format(color)
    return output

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
                delta_color="off",
                de
            )
        index += 1



    # st.dataframe(average_expenses, use_container_width=True)



    # All transactions
    st.subheader("All transactions", divider="rainbow")  
    styled_ledger_data = ledger_data.style.apply(highlight_alternate_months, axis=None)
    styled_ledger_data = styled_ledger_data.format({"Amount": "₹{:,.0f}"})
    st.dataframe(
        styled_ledger_data, 
        use_container_width=True, 
        hide_index=True,
        column_order=("Date", "Category", "Amount")
        )  

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