"""
Data Formatting Utilities
"""
from datetime import datetime
from typing import Optional


def format_timestamp(timestamp: str) -> str:
    """Format ISO timestamp to readable format"""
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp


def format_sensor_value(value: float, unit: str) -> str:
    """Format sensor value with unit"""
    return f"{value:.1f} {unit}"


def get_aqi_category(pm25: float) -> tuple[str, str]:
    """
    Get AQI category and color based on PM2.5 value
    Returns: (category, color)
    """
    from utils.constants import (
        PM25_GOOD, PM25_MODERATE, PM25_UNHEALTHY_SENSITIVE,
        PM25_UNHEALTHY, PM25_VERY_UNHEALTHY,
        COLOR_SUCCESS, COLOR_INFO, COLOR_WARNING, COLOR_DANGER
    )
    
    if pm25 <= PM25_GOOD:
        return "Good", COLOR_SUCCESS
    elif pm25 <= PM25_MODERATE:
        return "Moderate", COLOR_INFO
    elif pm25 <= PM25_UNHEALTHY_SENSITIVE:
        return "Unhealthy for Sensitive", COLOR_WARNING
    elif pm25 <= PM25_UNHEALTHY:
        return "Unhealthy", COLOR_DANGER
    elif pm25 <= PM25_VERY_UNHEALTHY:
        return "Very Unhealthy", COLOR_DANGER
    else:
        return "Hazardous", COLOR_DANGER


def get_risk_color(risk_level: str) -> str:
    """Get color for smoke risk level"""
    from utils.constants import COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER
    
    risk_colors = {
        "LOW": COLOR_SUCCESS,
        "MEDIUM": COLOR_WARNING,
        "HIGH": COLOR_DANGER
    }
    return risk_colors.get(risk_level.upper(), COLOR_INFO)


def get_confidence_emoji(confidence: float) -> str:
    """Get status text based on confidence level"""
    if confidence >= 0.8:
        return "[High]"
    elif confidence >= 0.5:
        return "[Medium]"
    else:
        return "[Low]"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
