import streamlit as st
from datetime import datetime  
import streamlit as st
import os
import shutil
import random
from PIL import Image, ImageDraw, ImageFilter


from sidebar import gen_sidebar

from data import load_ledger_data, load_schedule_data, format_indian, load_cabinet_data

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

def mask_circle_transparent(pil_img, blur_radius, offset=0):
    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    result = pil_img.copy()
    result.putalpha(mask)

    return result

def dashboard():  
    
    # st.title("Cat Management :orange[Dashboard]")  
    # st.image("https://placekitten.com/200/200", width=200)  
    # st.write("Cat Name: Fluffy")  # Replace with the cat's name  
    st.subheader(":green[{}] the Poonai".format("Mindy"), divider="orange")
    pic, data = st.columns([1, 1])
    with pic:
        image_path = None
        try:
            image_folder = "dataset/images/"
            images = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f)) and f != '.DS_Store']
            image_file = random.choice(images)
            image_path = os.path.join(image_folder, image_file)
            
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
            image_path  = "dataset/images/Mindy.png"
        
        image = Image.open(image_path)
        resized = crop_max_square(image).resize((300, 300), Image.LANCZOS)
        resized_circle = mask_circle_transparent(resized, 10)
        st.image(resized_circle)
         
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
            col_key, col_value = st.columns([2, 1])
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
