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
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background-color: #0E1117;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #1E1E1E;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00D9FF 0%, #0099CC 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 217, 255, 0.3);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
    }
    
    /* Cards */
    .element-container {
        transition: all 0.3s ease;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1E1E1E;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00D9FF;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #0099CC;
    }
    </style>
""", unsafe_allow_html=True)

# Main landing page
st.markdown("""
    <div style="text-align: center; padding: 60px 0 40px 0;">
        <h1 style="
            font-size: 64px;
            background: linear-gradient(135deg, #00D9FF 0%, #00C853 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        ">
            🌬️ VAYU AI
        </h1>
        <p style="color: #888; font-size: 20px; margin-top: 16px;">
            Gen-AI Powered Air Quality Monitoring System
        </p>
    </div>
""", unsafe_allow_html=True)

# Center button to dashboard
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Open Dashboard", use_container_width=True, type="primary"):
        st.switch_page("pages/1_📊_Dashboard.py")

st.markdown("<br><br>", unsafe_allow_html=True)

# Backend status check
from services.api_client import api_client

st.markdown("---")
st.markdown("### 🔌 System Status")

col1, col2 = st.columns(2)

with col1:
    try:
        health = api_client.health_check()
        st.success("✅ Backend Connected")
        st.caption(f"URL: `{os.getenv('BACKEND_URL', 'http://localhost:8000')}`")
    except Exception as e:
        st.error("❌ Backend Disconnected")
        st.caption(f"URL: `{os.getenv('BACKEND_URL', 'http://localhost:8000')}`")

with col2:
    try:
        devices = api_client.get_devices()
        st.info(f"📡 {len(devices)} Device(s) Connected" if devices else "📡 No Devices Found")
        if devices:
            st.caption(f"Devices: {', '.join(devices)}")
    except:
        st.warning("⚠️ Unable to fetch devices")

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 12px; padding: 20px;">
        VAYU AI v1.0.0 | Real-time Monitoring • AI Predictions • Blockchain Logging
    </div>
""", unsafe_allow_html=True)

