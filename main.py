# main.py
import streamlit as st
import os
import shutil
import zipfile

from pages.dashboard import dashboard
from pages.ledger import ledger
from pages.schedules import schedules

DATA_PATH = "dataset"

def main():

    _=st.set_page_config(
        page_title="Cat Management",
        page_icon="🐈",
        initial_sidebar_state="collapsed",
        layout="centered",
        ),

    page = st.sidebar.radio("Go to", ["Dashboard", "Ledger", "Schedules"])


    pages = {
        "Dashboard": dashboard,
        "Ledger": ledger,
        "Schedules": schedules,
    }

    # nav = st.selectbox("Go to", ["Dashboard", "Ledger", "Schedules"])
    # page = st.radio("Go to", ["Dashboard", "Ledger", "Schedules"])
    st.title(f"Cat Management :orange[{page}]")
    # nav = st.radio("Go to", ["Dashboard", "Ledger", "Schedules"])

    if page in pages:
        pages[page]()
    else:
        st.error("Something has gone wrong. Please contact the developer.")

    with st.sidebar:
        st.divider()

        # File uploader
        uploaded_files = st.file_uploader("Upload your cat photos", type=["png", "jpg", "jpeg"], accept_multiple_files=True) 
        for uploaded_file in uploaded_files:
            with open(os.path.join("dataset/images",uploaded_file.name),"wb") as f: 
                f.write(uploaded_file.getbuffer()) 

        st.divider()

        # Data controls
        st.subheader("Data Tools")
        type_of_data = st.radio(
            "Work with data:",
            ["Import", "Export", "Nuke"],
            index=0,
        )
        if type_of_data == 'Export':
            shutil.make_archive("cat-data", 'zip', DATA_PATH)
            with open("cat-data.zip", "rb") as fp:
                btn = st.download_button(
                    label="Download ZIP",
                    data=fp,
                    file_name="cat-data.zip",
                    mime="application/zip"
                )
        elif type_of_data == 'Import':
            import_zip_file = st.file_uploader('Upload zip file', accept_multiple_files=False, type='zip')
            if import_zip_file is not None:
                with zipfile.ZipFile(import_zip_file, "r") as z:
                    z.extractall(DATA_PATH)
        elif type_of_data == 'Nuke':
            if st.button('Deleta all data'):
                if os.path.exists(DATA_PATH) and os.path.isdir(DATA_PATH):
                    shutil.rmtree(DATA_PATH)




if __name__ == "__main__":
    main()