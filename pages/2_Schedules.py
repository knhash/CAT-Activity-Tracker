# schedules.py
import pandas as pd
import streamlit as st
from data import load_schedule_data, save_schedule_data
from sidebar import gen_sidebar

schedule_data_edited, schedule_data = None, None

def schedules():  
    global schedule_data_edited, schedule_data
    # st.title("Cat Management :orange[Schedules]")  

    # Input form  
    with st.form("schedule_form"):  
        date = st.date_input("Date")  
        description = st.text_input("Description")  
        is_active = st.checkbox("Active", value=True)  

        submit_button = st.form_submit_button("Add Schedule")  

    if submit_button:  
        new_schedule = pd.DataFrame([[date, description, is_active]], columns=["Date", "Description", "Active"])  
        schedule_data = load_schedule_data()  
        schedule_data = pd.concat([schedule_data, new_schedule], ignore_index=True)
        schedule_data.Date = pd.to_datetime(schedule_data.Date).dt.date
        save_schedule_data(schedule_data)  
  
    # Display schedule data  
    schedule_data = load_schedule_data()  
    st.subheader("All tasks", divider="rainbow")  
    schedule_data_edited = st.data_editor(
        schedule_data, 
        use_container_width=True, 
        hide_index=True,
    )
    if schedule_data_edited is not None:
        save_schedule_data(schedule_data_edited)
    
    
def main():

    _=st.set_page_config(
        page_title="CAT Activity Tracker",
        page_icon="🐈",
        initial_sidebar_state="collapsed",
        layout="centered",
        ),

    st.title(f"Cat Management :orange[Schedules]")

    schedules()

    with st.sidebar:
        gen_sidebar()
        
if __name__ == "__main__":
    main()