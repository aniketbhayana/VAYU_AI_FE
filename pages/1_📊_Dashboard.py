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

# Page config
st.set_page_config(page_title="Dashboard - VAYU AI", page_icon="📊", layout="wide")

# Header
st.title("📊 Real-Time Dashboard")
st.markdown("Monitor air quality, AI predictions, and system status in real-time")

# Sidebar controls
st.sidebar.header("Dashboard Controls")

# Device selector
try:
    devices = api_client.get_devices()
    if devices:
        selected_device = st.sidebar.selectbox(
            "Select Device",
            devices,
            index=0
        )
    else:
        selected_device = st.sidebar.text_input(
            "Device ID",
            value=os.getenv("DEFAULT_DEVICE_ID", "ESP32_001")
        )
        warning_alert("No devices found. Using default device ID.")
except Exception as e:
    selected_device = st.sidebar.text_input(
        "Device ID",
        value=os.getenv("DEFAULT_DEVICE_ID", "ESP32_001")
    )
    st.sidebar.error(f"Cannot fetch devices: {str(e)}")

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("Auto-refresh", value=True)
refresh_interval = int(os.getenv("REFRESH_INTERVAL", 5))

if auto_refresh:
    st.sidebar.info(f"🔄 Auto-refreshing every {refresh_interval} seconds")

# Manual refresh button
if st.sidebar.button("🔄 Refresh Now"):
    st.rerun()

st.sidebar.markdown("---")

# Manual override controls
st.sidebar.subheader("💨 Manual Fan Control")
override_enabled = st.sidebar.checkbox("Enable Manual Override")

if override_enabled:
    fan_on = st.sidebar.toggle("Fan ON/OFF", value=True)
    fan_intensity = st.sidebar.slider("Fan Intensity", 0, 100, 75, 5)
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("✅ Apply"):
            try:
                result = api_client.set_control_override(selected_device, fan_on, fan_intensity)
                st.success("Override applied!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col2:
        if st.button("❌ Clear"):
            try:
                result = api_client.clear_control_override(selected_device)
                st.success("Override cleared!")
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("---")

# Main dashboard content
try:
    # Fetch dashboard data
    with st.spinner("Loading dashboard data..."):
        # Try aggregated method (handles both implemented and fallback scenarios)
        dashboard_data = api_client.get_aggregated_dashboard_data(selected_device)
    
    # Extract data
    current_reading = dashboard_data.get("current_reading")
    prediction = dashboard_data.get("prediction")
    classification = dashboard_data.get("classification")
    control_status = dashboard_data.get("control_status")
    recent_faults = dashboard_data.get("recent_faults", [])
    system_health = dashboard_data.get("system_health", {})
    
    # Display current sensor readings
    if current_reading:
        st.subheader("📡 Current Sensor Readings")
        sensor_metric_row(
            pm25=current_reading.get("pm25", 0),
            co2=current_reading.get("co2", 0),
            co=current_reading.get("co", 0),
            voc=current_reading.get("voc", 0)
        )
        
        st.caption(f"Last updated: {current_reading.get('timestamp', 'N/A')}")
    else:
        info_alert("No current sensor readings available")
    
    st.markdown("---")
    
    # Two column layout for AQI and predictions
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if current_reading:
            st.subheader("🌡️ Air Quality Index")
            aqi_gauge(current_reading.get("pm25", 0))
    
    with col2:
        st.subheader("📈 Sensor History")
        try:
            history = api_client.get_sensor_history(selected_device, limit=20)
            if history:
                sensor_history_chart(history)
            else:
                info_alert("No historical data available")
        except Exception as e:
            error_alert(f"Cannot load sensor history: {str(e)}")
    
    st.markdown("---")
    
    # AI Predictions and Classifications
    col1, col2 = st.columns(2)
    
    with col1:
        if prediction:
            prediction_card(
                will_peak=prediction.get("will_peak", False),
                confidence=prediction.get("confidence", 0),
                reasoning=prediction.get("reasoning", "No analysis available"),
                estimated_peak=prediction.get("estimated_peak_value")
            )
        else:
            info_alert("🔥 Smoke prediction data not available")
    
    with col2:
        if classification:
            classification_card(
                air_type=classification.get("air_type", "unknown"),
                confidence=classification.get("confidence", 0),
                reasoning=classification.get("reasoning", "No analysis available")
            )
        else:
            info_alert("🏭 Air classification data not available")
    
    st.markdown("---")
    
    # Fault Detection and Control Status
    col1, col2 = st.columns(2)
    
    with col1:
        if recent_faults and len(recent_faults) > 0:
            latest_fault = recent_faults[0]
            fault_card(
                has_fault=latest_fault.get("has_fault", False),
                fault_type=latest_fault.get("fault_type", "no_fault"),
                severity=latest_fault.get("severity", "low"),
                details=latest_fault.get("details", ""),
                affected_sensor=latest_fault.get("affected_sensor")
            )
        else:
            fault_card(has_fault=False, fault_type="no_fault", severity="low", details="All systems operational")
    
    with col2:
        if control_status:
            control_card(
                fan_on=control_status.get("fan_on", False),
                fan_intensity=control_status.get("fan_intensity", 0),
                is_override=override_enabled
            )
        else:
            info_alert("💨 Control status not available")
    
    # System health footer
    if system_health:
        st.markdown("---")
        st.subheader("🏥 System Health")
        
        health_cols = st.columns(4)
        
        health_items = [
            ("Backend", system_health.get("status", "unknown")),
            ("Blockchain", system_health.get("blockchain", "unknown")),
            ("AI Agents", system_health.get("ai_agents", "unknown")),
            ("Sensors", system_health.get("sensors", "unknown"))
        ]
        
        for idx, (label, status) in enumerate(health_items):
            with health_cols[idx]:
                status_icon = "✅" if status in ["healthy", "connected", "ready", "active"] else "⚠️"
                st.metric(label, f"{status_icon} {status}")

except Exception as e:
    error_alert(f"Failed to load dashboard data: {str(e)}")
    st.info("💡 Make sure the backend is running and accessible")

# Auto-refresh logic
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()
