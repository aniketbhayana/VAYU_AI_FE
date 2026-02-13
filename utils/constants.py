"""
Constants and Configuration for VAYU AI Dashboard
"""

# API Endpoints
API_VERSION = "v1"

# Sensor thresholds for color coding
PM25_GOOD = 12.0
PM25_MODERATE = 35.5
PM25_UNHEALTHY_SENSITIVE = 55.5
PM25_UNHEALTHY = 150.5
PM25_VERY_UNHEALTHY = 250.5

CO2_GOOD = 800
CO2_MODERATE = 1000
CO2_UNHEALTHY = 1500

# Color scheme
COLOR_SUCCESS = "#00C853"
COLOR_WARNING = "#FFB300"
COLOR_DANGER = "#FF5252"
COLOR_INFO = "#00D9FF"
COLOR_BACKGROUND = "#0E1117"
COLOR_CARD = "#1E1E1E"

# Smoke risk levels
RISK_LOW = "LOW"
RISK_MEDIUM = "MEDIUM"
RISK_HIGH = "HIGH"

# Air types
AIR_TYPES = {
    "cigarette": "Cigarette Smoke",
    "vehicle": "Vehicle Exhaust",
    "cooking": "Cooking Fumes",
    "chemical": "Chemical Fumes",
    "clean": "Clean Air",
    "unknown": "Unknown"
}

# Fault types
FAULT_TYPES = {
    "sensor_stuck": "Sensor Stuck",
    "inconsistent_reading": "Inconsistent Reading",
    "fan_not_working": "Fan Not Working",
    "out_of_range": "Out of Range",
    "no_fault": "No Fault"
}

# Event types
EVENT_TYPES = {
    "decision": "Control Decision",
    "fault": "Fault Detected",
    "healing": "Self-Healing"
}
