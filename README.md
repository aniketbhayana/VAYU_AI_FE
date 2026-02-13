# 🌬️ VAYU AI - Frontend Dashboard

**Intelligent Air Quality Monitoring System**

A production-quality Streamlit dashboard for VAYU AI (AeroLedger) - a Gen-AI powered air monitoring system with real-time sensor data, AI predictions, fault detection, and blockchain logging.

---

## 🚀 Features

✅ **Real-time Monitoring** - Live sensor data (PM2.5, CO2, CO, VOC)  
✅ **AI Predictions** - Smoke event prediction with confidence scores  
✅ **Air Classification** - Identify pollution sources (cigarette, vehicle, cooking, chemical)  
✅ **Fault Detection** - Automatic sensor health monitoring  
✅ **Blockchain Logs** - Immutable event records  
✅ **Smart Controls** - Manual fan override with automatic mode  
✅ **Interactive Charts** - Plotly-powered visualizations  
✅ **Auto-refresh** - Configurable real-time updates  
✅ **Dark Theme** - Modern, professional UI  

---

## 📋 Prerequisites

- Python 3.8 or higher
- VAYU AI Backend running (default: `http://localhost:8000`)
- pip package manager

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/aniketbhayana/VAYU_AI_FE.git
cd VAYU_AI_FE
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
copy .env.example .env

# Edit .env and configure:
# - BACKEND_URL (default: http://localhost:8000)
# - REFRESH_INTERVAL (default: 5 seconds)
# - DEFAULT_DEVICE_ID (default: ESP32_001)
```

---

## 🎯 Quick Start

### Start the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Navigate the Dashboard

1. **Home** - Welcome page with backend status
2. **📊 Dashboard** - Real-time monitoring and controls
3. **🔗 Blockchain** - View transaction logs
4. **⚙️ Settings** - Configure preferences

---

## 📁 Project Structure

```
VAYU_AI_FE/
├── app.py                      # Main application entry point
├── pages/
│   ├── 1_📊_Dashboard.py       # Real-time monitoring dashboard
│   ├── 2_🔗_Blockchain.py      # Blockchain logs viewer
│   └── 3_⚙️_Settings.py        # Settings and configuration
├── components/
│   ├── metrics.py              # Metric display components
│   ├── status_cards.py         # Status card components
│   ├── charts.py               # Plotly chart components
│   └── alerts.py               # Alert/notification components
├── services/
│   └── api_client.py           # Backend API client
├── utils/
│   ├── constants.py            # Constants and configuration
│   └── formatters.py           # Data formatting utilities
├── assets/                     # Static assets (CSS, images)
├── .env                        # Environment configuration
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

---

## 🔌 Backend Integration

### API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Backend health check |
| `/api/v1/dashboard/devices` | GET | List registered devices |
| `/api/v1/dashboard/data/{device_id}` | GET | Aggregated dashboard data |
| `/api/v1/dashboard/blockchain/logs` | GET | Blockchain transaction logs |
| `/api/v1/sensor/history/{device_id}` | GET | Historical sensor readings |
| `/api/v1/control/status/{device_id}` | GET | Current control status |
| `/api/v1/control/override` | POST | Set manual fan control |
| `/api/v1/control/override/{device_id}` | DELETE | Clear manual override |

### Data Models

The frontend strictly follows backend data schemas:

- **SensorReading** - PM2.5, CO2, CO, VOC values
- **SmokePrediction** - AI prediction with confidence
- **AirTypeClassification** - Pollution source classification
- **FaultDetectionResult** - Sensor/system fault status
- **ControlResponse** - Fan control commands
- **BlockchainLog** - Immutable event records

---

## 🎨 Features Overview

### Dashboard Page

- **Live Metrics** - Real-time sensor values with color-coded AQI
- **AQI Gauge** - Visual air quality indicator
- **Sensor History Chart** - Time-series visualization
- **Smoke Prediction** - AI-powered risk assessment
- **Air Classification** - Pollution source identification
- **Fault Detection** - System health monitoring
- **Fan Control** - Manual override controls
- **Auto-refresh** - Configurable update interval

### Blockchain Page

- **Transaction Logs** - Immutable event records
- **Event Filtering** - Filter by type (decision, fault, healing)
- **Expandable Details** - View full event data
- **Table View** - Alternative data presentation
- **Hash Verification** - Blockchain integrity indicators

### Settings Page

- **Backend Configuration** - Set API URL
- **Dashboard Preferences** - Customize refresh interval
- **Connection Testing** - Verify backend connectivity
- **System Information** - Version and status details

---

## 🔧 Configuration

### Environment Variables

Edit `.env` file:

```bash
# Backend API URL
BACKEND_URL=http://localhost:8000

# Auto-refresh interval (seconds)
REFRESH_INTERVAL=5

# Default device to monitor
DEFAULT_DEVICE_ID=ESP32_001
```

### Customization

- **Colors** - Edit `utils/constants.py`
- **Thresholds** - Modify AQI ranges in `utils/constants.py`
- **Styling** - Custom CSS in `app.py`

---

## 🐛 Troubleshooting

### Backend Connection Failed

```
❌ Cannot connect to backend: http://localhost:8000
```

**Solution:**
1. Ensure backend server is running
2. Check `BACKEND_URL` in `.env`
3. Verify backend is accessible at the configured URL

### No Data Available

```
ℹ️ No current sensor readings available
```

**Solution:**
1. Check if devices are registered in backend
2. Verify device ID is correct
3. Ensure ESP32 is sending data to backend

### Import Errors

```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
pip install -r requirements.txt
```

---

## 🚀 Deployment

### Local Deployment

```bash
streamlit run app.py
```

### Production Deployment

For production deployment, consider:

1. **Streamlit Cloud** - Easy deployment from GitHub
2. **Docker** - Containerized deployment
3. **AWS/GCP/Azure** - Cloud platform hosting

Example Dockerfile:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 📚 Technology Stack

- **Frontend Framework:** Streamlit 1.31+
- **Charts:** Plotly 5.18+
- **HTTP Client:** Requests 2.31+
- **Data Processing:** Pandas 2.2+
- **Environment:** python-dotenv 1.0+

---

## 🔗 Related Repositories

- **Backend:** [VayuAi-YCH](https://github.com/Nihit-Garg/VayuAi-YCH)
- **Frontend:** [VAYU_AI_FE](https://github.com/aniketbhayana/VAYU_AI_FE.git)

---

## 📄 License

MIT License - See backend repository for details

---

## 👥 Contributors

Built for VAYU AI (AeroLedger) project

---

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check backend documentation
- Review API endpoint documentation at `http://localhost:8000/docs`

---

## 🎯 Roadmap

- [ ] WebSocket support for real-time updates
- [ ] Historical analytics dashboard
- [ ] Multi-device comparison view
- [ ] Export data to CSV/PDF
- [ ] Mobile-responsive improvements
- [ ] User authentication
- [ ] Custom alert thresholds

---

**Built with ❤️ for intelligent air quality management**
