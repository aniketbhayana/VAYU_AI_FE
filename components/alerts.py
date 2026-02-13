"""
Alert and Notification Components
"""
import streamlit as st


def connection_status(is_connected: bool, backend_url: str):
    """Display connection status banner"""
    if is_connected:
        st.success(f"Connected to backend: `{backend_url}`")
    else:
        st.error(f"Cannot connect to backend: `{backend_url}`")
        st.info("Make sure the backend server is running at the configured URL")


def error_alert(message: str):
    """Display error alert"""
    st.error(f"**Error:** {message}")


def warning_alert(message: str):
    """Display warning alert"""
    st.warning(f"**Warning:** {message}")


def info_alert(message: str):
    """Display info alert"""
    st.info(message)


def loading_placeholder(message: str = "Loading data..."):
    """Display loading spinner"""
    with st.spinner(message):
        pass
