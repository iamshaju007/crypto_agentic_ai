"""
Frontend Streamlit Application for Crypto AI Staking & Trading.

This module initializes the Streamlit app, sets up page configuration,
sidebar navigation, and routes to the Dashboard and Chatbot pages.
"""

# --- Standard Library Imports ---
from datetime import datetime

# --- Third-Party Imports ---
import streamlit as st

# --- Local Module Imports ---
try:
    from components.dashboard import render_dashboard  # Dashboard page
    from pages.chatbot import render_chatbot           # Chatbot page
except ImportError as e:
    st.error(f"⚠️ Module import error: {e}. Please ensure all necessary libraries are installed.")
    st.stop()  # Stop execution if modules are missing

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Crypto AI Staking & Trading",
    layout="wide"
)

# --- Sidebar Navigation ---
st.sidebar.title("Crypto AI App")
page = st.sidebar.radio("Navigate", ["Dashboard", "Chatbot"])

# --- API Base URL ---
API_BASE_URL = "http://backend:8000"

# --- Page Routing ---
if page == "Dashboard":
    st.title("Crypto Staking & Trading Dashboard")
    render_dashboard(API_BASE_URL)

elif page == "Chatbot":
    st.title("Crypto AI Chatbot")
    render_chatbot(API_BASE_URL)

# --- Sidebar Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown(
    f"🕒 **Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)
