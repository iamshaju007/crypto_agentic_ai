from datetime import datetime  # Standard library
import streamlit as st          # Third-party libraries

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Crypto AI Staking & Trading", layout="wide")

# --- Try-Except for Safe Module Imports ---
try:
    from components.dashboard import render_dashboard  # Local module
    from pages.chatbot import render_chatbot           # Local module
except ImportError as e:
    st.error(f"⚠️ Module import error: {e}. Please ensure all necessary libraries are installed.")
    st.stop()  # Stop execution if modules are missing

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

# --- Footer (Optional Enhancement) ---
st.sidebar.markdown("---")
st.sidebar.markdown(f"🕒 **Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
