# schedules.py
import pandas as pd
import streamlit as st
from data import load_cabinet_data, save_cabinet_data
from sidebar import gen_sidebar

cabinet_data = None

def schedules():  
    global cabinet_data

    # Input form  
    with st.form("cabinet_form"):  
        item = st.text_input("Item")  
        purpose = st.text_input("Purpose")  
        available = st.checkbox("Available", value=True)  

        submit_button = st.form_submit_button("Add Item")  

    if submit_button:  
        new_cabinet = pd.DataFrame([[item, purpose, available]], columns=["Item", "Purpose", "Available"])  
        cabinet_data = load_cabinet_data()  
        cabinet_data = pd.concat([cabinet_data, new_cabinet], ignore_index=True)
        save_cabinet_data(cabinet_data)  
  
    # Display schedule data  
    cabinet_data = load_cabinet_data()  
    st.subheader("All tasks", divider="rainbow")  
    cabinet_data_edited = st.data_editor(
        cabinet_data, 
        use_container_width=True, 
        hide_index=True,
        num_rows="dynamic",
        disabled=("Item", "Purpose")
    )
    if cabinet_data_edited is not None:
        save_cabinet_data(cabinet_data_edited)
    
    
def main():

    _=st.set_page_config(
        page_title="CAT Activity Tracker",
        page_icon="🐈",
        initial_sidebar_state="collapsed",
        layout="centered",
        ),

    st.title(f"Cat Management :orange[Cabinet]")

    schedules()

    with st.sidebar:
        gen_sidebar()
        
if __name__ == "__main__":
    main()