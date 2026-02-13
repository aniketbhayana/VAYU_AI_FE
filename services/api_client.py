"""
API Client for VAYU AI Backend
Handles all HTTP requests to the backend API
"""
import requests
import os
from typing import Optional, Dict, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class VayuAPIClient:
    """Client for interacting with VAYU AI backend API"""
    
    def __init__(self):
        self.base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        self.timeout = 10  # seconds
        
    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request to API"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {str(e)}")
    
    def _post(self, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make POST request to API"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, json=data, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {str(e)}")
    
    def _delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request to API"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.delete(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {str(e)}")
    
    # Health Check
    def health_check(self) -> Dict[str, Any]:
        """Check backend health status"""
        return self._get("/health")
    
    # Dashboard Endpoints
    def get_dashboard_data(self, device_id: str) -> Dict[str, Any]:
        """
        Get comprehensive dashboard data for a device
        Note: This endpoint may return 501 if not implemented
        """
        return self._get(f"/api/v1/dashboard/data/{device_id}")
    
    def get_devices(self) -> List[str]:
        """Get list of all registered devices"""
        response = self._get("/api/v1/dashboard/devices")
        return response.get("devices", [])
    
    def get_blockchain_logs(self, limit: int = 20) -> List[Dict]:
        """Get recent blockchain logs"""
        response = self._get("/api/v1/dashboard/blockchain/logs", params={"limit": limit})
        return response.get("logs", [])
    
    def get_analytics(self, device_id: str, hours: int = 24) -> Dict[str, Any]:
        """Get analytics for a device"""
        return self._get(f"/api/v1/dashboard/analytics/{device_id}", params={"hours": hours})
    
    # Sensor Endpoints
    def get_sensor_status(self, device_id: str) -> Dict[str, Any]:
        """Get current sensor status"""
        return self._get(f"/api/v1/sensor/status/{device_id}")
    
    def get_sensor_history(self, device_id: str, limit: int = 50) -> List[Dict]:
        """Get historical sensor readings"""
        response = self._get(f"/api/v1/sensor/history/{device_id}", params={"limit": limit})
        return response.get("readings", [])
    
    # Control Endpoints
    def get_control_status(self, device_id: str) -> Dict[str, Any]:
        """Get current control status"""
        return self._get(f"/api/v1/control/status/{device_id}")
    
    def set_control_override(self, device_id: str, fan_on: bool, fan_intensity: int) -> Dict[str, Any]:
        """Set manual control override"""
        return self._post(
            "/api/v1/control/override",
            params={
                "device_id": device_id,
                "fan_on": fan_on,
                "fan_intensity": fan_intensity
            }
        )
    
    def clear_control_override(self, device_id: str) -> Dict[str, Any]:
        """Clear manual override and return to automatic control"""
        return self._delete(f"/api/v1/control/override/{device_id}")
    
    # Aggregated data method (fallback if dashboard endpoint not ready)
    def get_aggregated_dashboard_data(self, device_id: str) -> Dict[str, Any]:
        """
        Aggregate data from multiple endpoints
        Fallback method if /api/v1/dashboard/data is not implemented
        """
        try:
            # Try the main dashboard endpoint first
            return self.get_dashboard_data(device_id)
        except Exception as e:
            # If it fails (501 or other error), aggregate manually
            try:
                # Get sensor history (most recent reading)
                history = self.get_sensor_history(device_id, limit=1)
                current_reading = history[0] if history else None
                
                # Get control status
                control_status = self.get_control_status(device_id)
                
                # Get blockchain logs
                logs = self.get_blockchain_logs(limit=10)
                
                # Construct aggregated response
                # Note: prediction, classification, and faults won't be available
                # unless backend implements those endpoints separately
                return {
                    "current_reading": current_reading,
                    "control_status": control_status,
                    "recent_logs": logs,
                    "system_health": {"status": "partial_data"},
                    # These will be None if not available
                    "prediction": None,
                    "classification": None,
                    "recent_faults": []
                }
            except Exception as agg_error:
                raise Exception(f"Failed to aggregate data: {str(agg_error)}")


# Global API client instance
api_client = VayuAPIClient()
