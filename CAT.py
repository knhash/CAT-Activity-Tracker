# main.py
import streamlit as st

from dashboard import dashboard

from sidebar import gen_sidebar


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