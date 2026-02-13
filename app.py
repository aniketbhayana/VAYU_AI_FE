"""
VAYU AI - Air Quality Monitoring Dashboard
Main Application Entry Point
"""
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="VAYU AI - Air Quality Monitor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for black theme and top navigation
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container - Solid Black */
    .stApp {
        background-color: #000000 !important;
    }
    
    /* Hide default header and footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Buttons - Gradient (Normal Green to Dark Green) */
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3) !important;
    }
    
    /* Beige Navigation Styling */
    .top-nav-bar {
        background-color: #F5F5DC;
        padding: 5px;
        border-radius: 4px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# Render Top Navigation
from utils.navigation import render_top_nav
render_top_nav()

# Main landing page
st.markdown("""
    <div style="text-align: center; padding: 100px 0 40px 0;">
        <h1 style="
            font-size: 80px;
            color: #FFFFFF !important;
            margin: 0;
            font-weight: 800;
        ">
            VAYU AI
        </h1>
        <p style="color: #AAAAAA; font-size: 24px; margin-top: 16px;">
            Gen-AI Powered Air Quality Monitoring System
        </p>
    </div>
""", unsafe_allow_html=True)

# Center button to dashboard
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    # Gradient button, no emoji/logo
    if st.button("Open Dashboard", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Dashboard.py")

st.markdown("<br><br>", unsafe_allow_html=True)

# Backend status check
from services.api_client import api_client

st.markdown("<h3 style='text-align: center;'>System Status</h3>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([1, 2, 2, 1])

with col2:
    try:
        health = api_client.health_check()
        st.success("Backend Connected")
    except Exception as e:
        st.error("Backend Disconnected")

with col3:
    try:
        devices = api_client.get_devices()
        status_text = f"Device(s) Connected: {len(devices)}" if devices else "No Devices Found"
        st.info(status_text)
    except:
        st.warning("Device check unavailable")

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #444; font-size: 14px; padding: 20px;">
        VAYU AI v1.1.0 | Reliable Environment Intelligence
    </div>
""", unsafe_allow_html=True)


