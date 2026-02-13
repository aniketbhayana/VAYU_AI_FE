"""
Reusable Metric Display Components
"""
import streamlit as st
from typing import Optional


def metric_card(label: str, value: str, unit: str = "", delta: Optional[str] = None, color: str = "#00D9FF"):
    """
    Display a metric card with label, value, and optional delta
    
    Args:
        label: Metric label
        value: Metric value
        unit: Unit of measurement
        delta: Optional delta value
        color: Color for the metric
    """
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {color}15 0%, {color}05 100%);
            border-left: 4px solid {color};
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
        ">
            <div style="color: #888; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">
                {label}
            </div>
            <div style="color: {color}; font-size: 32px; font-weight: 700; margin: 8px 0;">
                {value}<span style="font-size: 16px; margin-left: 4px;">{unit}</span>
            </div>
            {f'<div style="color: #888; font-size: 14px;">{delta}</div>' if delta else ''}
        </div>
    """, unsafe_allow_html=True)


def sensor_metric_row(pm25: float, co2: float, co: float, voc: float):
    """Display all sensor metrics in a row"""
    from utils.formatters import get_aqi_category
    from utils.constants import COLOR_INFO, COLOR_WARNING
    
    col1, col2, col3, col4 = st.columns(4)
    
    # PM2.5 with AQI category
    category, color = get_aqi_category(pm25)
    with col1:
        metric_card("PM2.5", f"{pm25:.1f}", "µg/m³", category, color)
    
    # CO2
    co2_color = COLOR_WARNING if co2 > 1000 else COLOR_INFO
    with col2:
        metric_card("CO2", f"{co2:.0f}", "ppm", color=co2_color)
    
    # CO
    with col3:
        metric_card("CO", f"{co:.1f}", "ppm", color=COLOR_INFO)
    
    # VOC
    with col4:
        metric_card("VOC", f"{voc:.0f}", "ppb", color=COLOR_INFO)


def large_metric(label: str, value: str, icon: str = "", color: str = "#00D9FF"):
    """Display a large centered metric"""
    st.markdown(f"""
        <div style="
            text-align: center;
            padding: 24px;
            background: linear-gradient(135deg, {color}20 0%, {color}05 100%);
            border-radius: 12px;
            margin: 16px 0;
        ">
            {f'<div style="font-size: 48px; margin-bottom: 8px;">{icon}</div>' if icon else ''}
            <div style="color: #888; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">
                {label}
            </div>
            <div style="color: {color}; font-size: 48px; font-weight: 700; margin-top: 8px;">
                {value}
            </div>
        </div>
    """, unsafe_allow_html=True)
