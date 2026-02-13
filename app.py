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

# Main header
st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="
            font-size: 48px;
            background: linear-gradient(135deg, #00D9FF 0%, #00C853 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        ">
            🌬️ VAYU AI
        </h1>
        <p style="color: #888; font-size: 16px; margin-top: 8px;">
            Intelligent Air Quality Monitoring System
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Welcome message
st.markdown("""
### Welcome to VAYU AI Dashboard

This is the main landing page. Use the sidebar to navigate to:

- **📊 Dashboard** - Real-time air quality monitoring and control
- **🔗 Blockchain** - View blockchain transaction logs
- **⚙️ Settings** - Configure dashboard settings

---

### System Overview

**VAYU AI** (AeroLedger) is a Gen-AI powered intelligent air monitoring system featuring:

✅ **Real-time Sensor Monitoring** - PM2.5, CO2, CO, VOC  
✅ **AI-Powered Predictions** - Smoke event prediction  
✅ **Air Classification** - Identify pollution sources  
✅ **Fault Detection** - Automatic sensor health monitoring  
✅ **Self-Healing** - Intelligent recovery from faults  
✅ **Blockchain Logging** - Immutable event records  
✅ **Smart Fan Control** - Automated air quality management  

---

### Quick Start

1. Ensure the backend server is running at `http://localhost:8000`
2. Navigate to **📊 Dashboard** to view real-time data
3. Select your device from the dropdown
4. Monitor air quality metrics and AI predictions
5. Use manual override controls if needed

---

### Backend Status
""")

# Check backend connection
from services.api_client import api_client
from components.alerts import connection_status

try:
    health = api_client.health_check()
    connection_status(True, os.getenv("BACKEND_URL", "http://localhost:8000"))
    
    st.json(health)
    
except Exception as e:
    connection_status(False, os.getenv("BACKEND_URL", "http://localhost:8000"))
    st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 12px; padding: 20px;">
        VAYU AI Dashboard v1.0.0 | Built with Streamlit | © 2026
    </div>
""", unsafe_allow_html=True)
