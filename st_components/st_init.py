import streamlit as st
import json

def set_style():    
    # PAGE CONFIG
    st.set_page_config(
        page_title="Open-Interpreter Gpt App",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # STYLES
    st.markdown(
    """<style>.eczjsme4 {
            padding: 4rem 1rem;
            }
            .css-w770g5{
            width: 100%;}
            .css-b3z5c9{
            width: 100%;}
            .stButton>button{
            width: 100%;}
            .stDownloadButton>button{
            width: 100%;}
            button[data-testid="baseButton-primary"]{
            border-color: #505050;
            background-color: #1E1E1E;
            }
            button[data-testid="baseButton-primary"]:hover {
            border-color: #FC625F;
            background-color: #1E1E1E;
            color: #FC625F;
            }
            </style>""", 
        unsafe_allow_html=True
    )