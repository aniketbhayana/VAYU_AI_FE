"""
Settings Page
Configure dashboard settings and preferences
"""
import streamlit as st
import os
from dotenv import load_dotenv, set_key

# Load environment
load_dotenv()

# Page config
st.set_page_config(page_title="Settings - VAYU AI", page_icon="⚙️", layout="wide")

# Header
st.title("⚙️ Dashboard Settings")
st.markdown("Configure backend connection and dashboard preferences")

st.markdown("---")

# Backend Configuration
st.subheader("🔌 Backend Configuration")

col1, col2 = st.columns(2)

with col1:
    backend_url = st.text_input(
        "Backend URL",
        value=os.getenv("BACKEND_URL", "http://localhost:8000"),
        help="URL of the VAYU AI backend server"
    )

with col2:
    default_device = st.text_input(
        "Default Device ID",
        value=os.getenv("DEFAULT_DEVICE_ID", "ESP32_001"),
        help="Default device to monitor"
    )

# Dashboard Preferences
st.markdown("---")
st.subheader("🎨 Dashboard Preferences")

col1, col2 = st.columns(2)

with col1:
    refresh_interval = st.number_input(
        "Auto-refresh Interval (seconds)",
        min_value=1,
        max_value=60,
        value=int(os.getenv("REFRESH_INTERVAL", 5)),
        help="How often to refresh dashboard data"
    )

with col2:
    chart_history_limit = st.number_input(
        "Chart History Limit",
        min_value=10,
        max_value=100,
        value=20,
        help="Number of historical data points to show in charts"
    )

# Save settings
st.markdown("---")

if st.button("💾 Save Settings", type="primary"):
    try:
        # Update .env file
        env_file = ".env"
        
        set_key(env_file, "BACKEND_URL", backend_url)
        set_key(env_file, "DEFAULT_DEVICE_ID", default_device)
        set_key(env_file, "REFRESH_INTERVAL", str(refresh_interval))
        
        st.success("✅ Settings saved successfully!")
        st.info("🔄 Please refresh the page for changes to take effect")
        
    except Exception as e:
        st.error(f"❌ Failed to save settings: {str(e)}")

# System Information
st.markdown("---")
st.subheader("ℹ️ System Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Dashboard Version**  
    v1.0.0
    """)

with col2:
    st.markdown(f"""
    **Backend URL**  
    `{os.getenv("BACKEND_URL", "Not configured")}`
    """)

with col3:
    st.markdown(f"""
    **Default Device**  
    `{os.getenv("DEFAULT_DEVICE_ID", "Not configured")}`
    """)

# Test Connection
st.markdown("---")
st.subheader("🔍 Test Backend Connection")

if st.button("Test Connection"):
    from services.api_client import api_client
    
    try:
        with st.spinner("Testing connection..."):
            health = api_client.health_check()
        
        st.success("✅ Backend connection successful!")
        st.json(health)
        
    except Exception as e:
        st.error(f"❌ Connection failed: {str(e)}")
        st.info("💡 Make sure the backend server is running at the configured URL")

# About
st.markdown("---")
st.subheader("📖 About VAYU AI")

st.markdown("""
**VAYU AI (AeroLedger)** is a Gen-AI powered intelligent air monitoring system featuring:

- 🌡️ Real-time sensor data processing (PM2.5, CO2, CO, VOC)
- 🤖 AI-powered smoke prediction and air classification
- 🔧 Fault detection and self-healing capabilities
- 🔗 Blockchain logging for immutable event records
- 💨 Intelligent fan control decisions
- 📊 Real-time dashboard visualization

**Technology Stack:**
- Frontend: Streamlit + Plotly
- Backend: FastAPI + Python
- AI: LLM-powered agents
- Blockchain: Ethereum (optional)

**Repositories:**
- Backend: [VayuAi-YCH](https://github.com/Nihit-Garg/VayuAi-YCH)
- Frontend: [VAYU_AI_FE](https://github.com/aniketbhayana/VAYU_AI_FE.git)

---

© 2026 VAYU AI Team | Built for intelligent air quality management
""")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 12px; padding: 20px;">
        For support or issues, please visit our GitHub repositories
    </div>
""", unsafe_allow_html=True)
