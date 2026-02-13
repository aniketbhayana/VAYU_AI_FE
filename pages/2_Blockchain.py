"""
Blockchain Logs Page
View immutable blockchain transaction logs
"""
import streamlit as st
import pandas as pd
from datetime import datetime

from services.api_client import api_client
from components.alerts import error_alert, info_alert
from utils.constants import EVENT_TYPES
from utils.formatters import format_timestamp

# Page config
st.set_page_config(page_title="Blockchain Logs - VAYU AI", layout="wide")

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
st.title("Blockchain Transaction Logs")
st.markdown("<p style='color: #AAAAAA;'>View immutable records of critical system events</p>", unsafe_allow_html=True)

# Filter Controls Row (instead of sidebar)
col1, col2, col3 = st.columns([2, 3, 1])
with col1:
    log_limit = st.slider("Number of logs", 10, 100, 20, 10)

with col2:
    event_filter = st.multiselect(
        "Filter Event Types",
        options=["decision", "fault", "healing"],
        default=["decision", "fault", "healing"]
    )

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Refresh Logs", use_container_width=True):
        st.rerun()

st.markdown("---")

# Fetch and display logs
try:
    with st.spinner("Loading blockchain logs..."):
        logs = api_client.get_blockchain_logs(limit=log_limit)
    
    if not logs:
        info_alert("No blockchain logs found")
    else:
        # Filter by event type
        if event_filter:
            logs = [log for log in logs if log.get("event_type") in event_filter]
        
        st.success(f"Loaded {len(logs)} blockchain logs")
        
        # Display summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        decision_count = sum(1 for log in logs if log.get("event_type") == "decision")
        fault_count = sum(1 for log in logs if log.get("event_type") == "fault")
        healing_count = sum(1 for log in logs if log.get("event_type") == "healing")
        
        with col1:
            st.metric("Total Logs", len(logs))
        with col2:
            st.metric("Decisions", decision_count)
        with col3:
            st.metric("Faults", fault_count)
        with col4:
            st.metric("Healing", healing_count)
        
        st.markdown("---")
        
        # Display logs as expandable cards
        st.subheader("Transaction Log Entries")
        
        for idx, log in enumerate(logs):
            event_type = log.get("event_type", "unknown")
            timestamp = format_timestamp(log.get("timestamp", ""))
            device_id = log.get("device_id", "N/A")
            tx_hash = log.get("hash", "N/A")
            data = log.get("data", {})
            
            with st.expander(f"{event_type.upper()} - {timestamp} - Device: {device_id}", expanded=(idx < 3)):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown(f"""
                    **Event Type:** {event_type}  
                    **Timestamp:** {timestamp}  
                    **Device ID:** `{device_id}`  
                    **TX Hash:** `{tx_hash[:16]}...`
                    """)
                
                with col2:
                    st.markdown("**Event Data:**")
                    st.json(data)
        
        st.markdown("---")
        
        # Optional: Display as table
        if st.checkbox("Show as Table"):
            df_logs = pd.DataFrame(logs)
            
            # Format timestamp column if exists
            if 'timestamp' in df_logs.columns:
                df_logs['timestamp'] = df_logs['timestamp'].apply(format_timestamp)
            
            # Display selected columns
            display_columns = ['event_type', 'timestamp', 'device_id', 'hash']
            available_columns = [col for col in display_columns if col in df_logs.columns]
            
            st.dataframe(
                df_logs[available_columns],
                use_container_width=True,
                hide_index=True
            )

except Exception as e:
    error_alert(f"Failed to load blockchain logs: {str(e)}")
    st.info("Make sure the backend is running and the blockchain logger is active")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 14px; padding: 20px;">
        Blockchain logs are immutable and cryptographically verified
    </div>
""", unsafe_allow_html=True)
