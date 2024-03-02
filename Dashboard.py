# main.py
import streamlit as st
# dashboard.py
from datetime import datetime  
import streamlit as st
import os
import shutil
import random

from sidebar import gen_sidebar

from data import load_ledger_data, load_schedule_data, format_indian, load_cabinet_data

def dashboard():  
    
    # st.title("Cat Management :orange[Dashboard]")  
    # st.image("https://placekitten.com/200/200", width=200)  
    # st.write("Cat Name: Fluffy")  # Replace with the cat's name  
    st.subheader(":green[{}] the Poonai".format("Mindy"), divider="orange")
    pic, data = st.columns([1, 1])
    with pic:
        try:
            image_folder = "dataset/images/"
            images = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
            image_file = random.choice(images)
            st.image(os.path.join(image_folder, image_file), use_column_width=True)
        except:
            # Check if the image exists in the dataset
            if not os.path.exists("dataset/images/Mindy.png"):
                # Create the directory if it doesn't exist
                if not os.path.exists("dataset/images"):
                    os.makedirs("dataset/images")
                # Copy the default image to the dataset
                shutil.copy("Mindy.png", "dataset/images/Mindy.png")
                if not os.path.exists("dataset/csvs"):
                    os.makedirs("dataset/csvs")

            st.image("dataset/images/Mindy.png", use_column_width=True)
         
    with data:
        details = '''
        {
            "name": "someshwara poonai",
            "nickname": "mindy",
            "gender": "female",
            "breed": "domestic shorthair",
            "color": "calico",
            "age": "1.5 years",
            "weight": "3.0 kg",
            

            "cute": "💯",
        }
        '''
        st.json(details)
        
        
    
  
    # Load ledger and schedule data  
    ledger_data = load_ledger_data()  
    schedule_data = load_schedule_data()  
    cabinet_data = load_cabinet_data()

    st.divider()        

  
    # Calculate and display dashboard data  

    if not schedule_data.empty:  
        next_schedule = schedule_data.loc[schedule_data["Date"] >= datetime.now().date()].sort_values(by="Date").iloc[0]  
        col_key, col_value = st.columns([2, 1])
        col_key.subheader(f"Task :green[{next_schedule.Description}] is scheduled")
        col_value.subheader(f"`{next_schedule.Date.strftime('%d %B %Y')}`")

    if not cabinet_data.empty:
        unavailable_items = cabinet_data[~cabinet_data.Available].Item.to_list()
        if unavailable_items:
            
            col_key.subheader(f"Cabinet :green[Exhausted]")
            col_value.subheader(f"`{unavailable_items}`")

    if not ledger_data.empty:  
        total_expenses = ledger_data["Amount"].sum()  
        col_key, col_value = st.columns([2, 1])
        col_key.subheader(f"Net expenses :green[YTD]")
        col_value.subheader(f"`₹{format_indian(total_expenses)}`")


   

def main():

    _=st.set_page_config(
        page_title="CAT Activity Tracker",
        page_icon="🐈",
        initial_sidebar_state="collapsed",
        layout="centered",
        ),

    st.title(f"Cat Management :orange[Dashboard]")

    dashboard()

    with st.sidebar:
        gen_sidebar()




if __name__ == "__main__":
    main()