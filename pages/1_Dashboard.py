"""
Dashboard Page - Real-time Air Quality Monitoring
"""
import streamlit as st
import time
import os
from datetime import datetime
from dotenv import load_dotenv

from services.api_client import api_client
from components.metrics import sensor_metric_row
from components.status_cards import prediction_card, classification_card, fault_card, control_card
from components.charts import sensor_history_chart, aqi_gauge
from components.alerts import error_alert, warning_alert, info_alert

# Load environment
load_dotenv()

# Page config - Page title is rendered by Streamlit based on file name or set_page_config
st.set_page_config(page_title="Dashboard - VAYU AI", layout="wide")

# Custom CSS for black theme and hiding sidebar
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] { display: none; }
    h1, h2, h3 { color: #FFFFFF !important; }
    
    /* Gradient styling for all buttons on this page */
    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Top Navigation
from utils.navigation import render_top_nav
render_top_nav()

# Header
st.title("Real-Time Dashboard")
st.markdown("<p style='color: #AAAAAA;'>Monitoring air quality, AI predictions, and system health</p>", unsafe_allow_html=True)

# Controls Row (Simplified)
col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
with col1:
    try:
        devices = api_client.get_devices()
        selected_device = st.selectbox("Device Selection", devices if devices else ["ESP32_001"])
    except:
        selected_device = st.text_input("Device ID", value="ESP32_001")

with col2:
    auto_refresh = st.checkbox("Enable Auto-refresh", value=True)
    refresh_interval = 5

with col3:
    if st.button("Trigger Manual Refresh", use_container_width=True):
        st.rerun()

st.markdown("---")

# DATA RETRIEVAL (The "Opportunity" to link backend data)
dashboard_data = {}
fetch_error = None
try:
    # This is where the backend linking happens
    dashboard_data = api_client.get_aggregated_dashboard_data(selected_device)
except Exception as e:
    fetch_error = str(e)

# 1. Real-Time Sensor Data Section (Heading is Permanent)
st.subheader("Real-Time Sensor Data (ESP32)")
sensor_container = st.container()
with sensor_container:
    current_reading = dashboard_data.get("current_reading")
    if current_reading:
        sensor_metric_row(
            pm25=current_reading.get("pm25", 0),
            co2=current_reading.get("co2", 0),
            co=current_reading.get("co", 0),
            voc=current_reading.get("voc", 0)
        )
    else:
        st.info("Reading live data stream... (Waiting for sensor connection)")

st.markdown("---")

# 2. AQI and Trends Section
col1, col2 = st.columns(2)

with col1:
    st.subheader("Air Quality Index (AQI)")
    if current_reading:
        aqi_gauge(current_reading.get("pm25", 0))
    else:
        st.caption("Awaiting data for AQI calculation")

with col2:
    st.subheader("Historical Sensor Trends")
    try:
        history = api_client.get_sensor_history(selected_device, limit=20)
        if history:
            sensor_history_chart(history)
        else:
            st.caption("Gathering historical data points...")
    except:
        st.caption("Trend visualization unavailable")

st.markdown("---")

# 3. Gen-AI Agent Predictions Section
st.subheader("Gen-AI Agent Predictions")
col_ai1, col_ai2 = st.columns(2)

with col_ai1:
    prediction = dashboard_data.get("prediction")
    if prediction:
        prediction_card(
            will_peak=prediction.get("will_peak", False),
            confidence=prediction.get("confidence", 0),
            reasoning=prediction.get("reasoning", "Analysis in progress..."),
            estimated_peak=prediction.get("estimated_peak_value")
        )
    else:
        info_alert("Agent is analyzing environment for smoke risk...")

with col_ai2:
    classification = dashboard_data.get("classification")
    if classification:
        classification_card(
            air_type=classification.get("air_type", "unknown"),
            confidence=classification.get("confidence", 0),
            reasoning=classification.get("reasoning", "Identifying pollution sources...")
        )
    else:
        info_alert("Agent is classifying current air components...")

st.markdown("---")

# 4. System Health & Control Section
st.subheader("System Health & Control")
col_ctrl1, col_ctrl2 = st.columns(2)

with col_ctrl1:
    recent_faults = dashboard_data.get("recent_faults", [])
    if recent_faults:
        latest_fault = recent_faults[0]
        fault_card(
            has_fault=latest_fault.get("has_fault", False),
            fault_type=latest_fault.get("fault_type", "no_fault"),
            severity=latest_fault.get("severity", "low"),
            details=latest_fault.get("details", ""),
            affected_sensor=latest_fault.get("affected_sensor")
        )
    else:
        fault_card(has_fault=False, fault_type="no_fault", severity="low", details="Monitoring hardware integrity...")

with col_ctrl2:
    control_status = dashboard_data.get("control_status")
    if control_status:
        control_card(
            fan_on=control_status.get("fan_on", False),
            fan_intensity=control_status.get("fan_intensity", 0),
            is_override=False # Default to auto
        )
    else:
        info_alert("Fan control synchronization in progress...")

# Footer Status
if fetch_error:
    st.markdown("<br>", unsafe_allow_html=True)
    st.warning(f"Backend Sync: {fetch_error}")

# Auto-refresh logic
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()
