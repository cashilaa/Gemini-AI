import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
    .big-font {
        font-size:36px !important;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
    }
    .stApp {
        background-color: #2C2C2C;
        color: #E0E0E0 !important;
    }
    body {
        color: #E0E0E0;
    }
    p, .stMarkdown, .stText {
        color: #E0E0E0 !important;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stSelectbox {
        background-color: #3C3C3C;
    }
    </style>
    """, unsafe_allow_html=True)