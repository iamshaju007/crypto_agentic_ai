import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from components.dashboard import render_dashboard
from pages.chatbot import render_chatbot

st.set_page_config(page_title="Crypto AI Staking & Trading", layout="wide")

# Sidebar for navigation
st.sidebar.title("Crypto AI App")
page = st.sidebar.radio("Navigate", ["Dashboard", "Chatbot"])

# API base URL
API_BASE_URL = "http://backend:8000"

# Dashboard page
if page == "Dashboard":
    st.title("Crypto Staking & Trading Dashboard")
    render_dashboard(API_BASE_URL)

# Chatbot page
elif page == "Chatbot":
    st.title("Crypto AI Chatbot")
    render_chatbot(API_BASE_URL)