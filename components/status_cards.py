"""
Status Card Components
"""
import streamlit as st
from typing import Optional


def status_card(title: str, content: str, icon: str = "ℹ️", color: str = "#00D9FF", expandable: bool = False):
    """
    Display a status card with title and content
    
    Args:
        title: Card title
        content: Card content
        icon: Icon emoji
        color: Border color
        expandable: Whether content should be in an expander
    """
    st.markdown(f"""
        <div style="
            background: #1E1E1E;
            border-left: 4px solid {color};
            border-radius: 8px;
            padding: 16px;
            margin: 12px 0;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 24px; margin-right: 12px;">{icon}</span>
                <span style="color: {color}; font-size: 18px; font-weight: 600;">{title}</span>
            </div>
    """, unsafe_allow_html=True)
    
    if expandable:
        with st.expander("Details", expanded=False):
            st.markdown(content)
    else:
        st.markdown(f'<div style="color: #CCC; line-height: 1.6;">{content}</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def prediction_card(will_peak: bool, confidence: float, reasoning: str, estimated_peak: Optional[float] = None):
    """Display smoke prediction card"""
    from utils.formatters import get_confidence_emoji, get_risk_color
    from utils.constants import RISK_LOW, RISK_MEDIUM, RISK_HIGH
    
    # Determine risk level
    if will_peak and confidence > 0.7:
        risk = RISK_HIGH
    elif will_peak and confidence > 0.4:
        risk = RISK_MEDIUM
    else:
        risk = RISK_LOW
    
    color = get_risk_color(risk)
    emoji = get_confidence_emoji(confidence)
    
    content = f"""
    <strong>Risk Level:</strong> {emoji} {risk} ({confidence*100:.0f}% confidence)<br/>
    <strong>Will Peak:</strong> {'Yes' if will_peak else 'No'}<br/>
    {f'<strong>Estimated Peak:</strong> {estimated_peak:.1f} µg/m³<br/>' if estimated_peak else ''}
    <strong>AI Analysis:</strong> {reasoning}
    """
    
    status_card("🔥 Smoke Prediction", content, "🔥", color)


def classification_card(air_type: str, confidence: float, reasoning: str):
    """Display air classification card"""
    from utils.constants import AIR_TYPES, COLOR_INFO, COLOR_SUCCESS
    from utils.formatters import get_confidence_emoji
    
    air_label = AIR_TYPES.get(air_type, air_type)
    emoji = get_confidence_emoji(confidence)
    color = COLOR_SUCCESS if air_type == "clean" else COLOR_INFO
    
    content = f"""
    <strong>Type:</strong> {air_label}<br/>
    <strong>Confidence:</strong> {emoji} {confidence*100:.0f}%<br/>
    <strong>AI Analysis:</strong> {reasoning}
    """
    
    status_card("🏭 Air Classification", content, "🏭", color)


def fault_card(has_fault: bool, fault_type: str, severity: str, details: str, affected_sensor: Optional[str] = None):
    """Display fault detection card"""
    from utils.constants import FAULT_TYPES, COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER
    
    if not has_fault:
        status_card("⚠️ Fault Detection", "✅ <strong>All Systems Healthy</strong>", "✅", COLOR_SUCCESS)
        return
    
    # Determine color based on severity
    severity_colors = {
        "low": COLOR_WARNING,
        "medium": COLOR_WARNING,
        "high": COLOR_DANGER
    }
    color = severity_colors.get(severity, COLOR_WARNING)
    
    fault_label = FAULT_TYPES.get(fault_type, fault_type)
    
    content = f"""
    <strong>Status:</strong> ❌ Fault Detected<br/>
    <strong>Type:</strong> {fault_label}<br/>
    <strong>Severity:</strong> {severity.upper()}<br/>
    {f'<strong>Affected Sensor:</strong> {affected_sensor.upper()}<br/>' if affected_sensor else ''}
    <strong>Details:</strong> {details}
    """
    
    status_card("⚠️ Fault Detection", content, "⚠️", color)


def control_card(fan_on: bool, fan_intensity: int, is_override: bool = False):
    """Display fan control status card"""
    from utils.constants import COLOR_SUCCESS, COLOR_INFO
    
    color = COLOR_SUCCESS if fan_on else COLOR_INFO
    status_icon = "🟢" if fan_on else "⚫"
    
    content = f"""
    <strong>Status:</strong> {status_icon} {'ON' if fan_on else 'OFF'}<br/>
    <strong>Speed:</strong> {fan_intensity}%<br/>
    <strong>Mode:</strong> {'🔧 Manual Override' if is_override else '🤖 Automatic'}
    """
    
    status_card("💨 Fan Control", content, "💨", color)
