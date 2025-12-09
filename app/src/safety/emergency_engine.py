"""
Emergency & Safety Engine Module
Detects dangerous situations and triggers emergency responses
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from src.types import Alert, AlertSeverity, SensorData


class EmergencyEngine:
    """
    Monitors for emergency situations including falls, screams, and abnormal motion.
    Triggers alerts and emergency responses when danger is detected.
    """
    
    def __init__(self, emergency_callback: Optional[Callable] = None):
        self.emergency_callback = emergency_callback
        
        # Alert management
        self.active_alerts: List[Alert] = []
        self.alert_history: List[Alert] = []
        
        # Emergency state
        self.emergency_mode_active = False
        self.fall_detected_timestamp: Optional[datetime] = None
        self.scream_detected_timestamp: Optional[datetime] = None
        
        # Configuration
        self.fall_confirmation_delay_seconds = 2
        self.alert_cooldown_seconds = 30
        self.emergency_contacts: List[str] = []
    
    def add_emergency_contact(self, contact_info: str):
        """Add emergency contact"""
        if contact_info not in self.emergency_contacts:
            self.emergency_contacts.append(contact_info)
    
    def remove_emergency_contact(self, contact_info: str):
        """Remove emergency contact"""
        if contact_info in self.emergency_contacts:
            self.emergency_contacts.remove(contact_info)
    
    def analyze_sensor_data(self, sensor_data: SensorData) -> List[Alert]:
        """Analyze sensor data for emergencies"""
        alerts = []
        
        # Fall detection
        if sensor_data.fall_detected:
            fall_alert = self._handle_fall_detection(sensor_data)
            if fall_alert:
                alerts.append(fall_alert)
        
        # Scream detection
        if sensor_data.scream_detected:
            scream_alert = self._handle_scream_detection(sensor_data)
            if scream_alert:
                alerts.append(scream_alert)
        
        # Abnormal motion (ongoing convulsions, seizures)
        if sensor_data.abnormal_motion:
            if not self._is_user_actively_moving(sensor_data):
                motion_alert = self._create_alert(
                    "Abnormal Motion Detected",
                    "Unusual motion pattern detected. Are you safe?",
                    AlertSeverity.WARNING
                )
                alerts.append(motion_alert)
        
        return alerts
    
    def _handle_fall_detection(self, sensor_data: SensorData) -> Optional[Alert]:
        """Handle fall detection with confirmation delay"""
        if not self.fall_detected_timestamp:
            # First detection, start confirmation delay
            self.fall_detected_timestamp = datetime.now()
            return None
        
        # Check if confirmation threshold reached
        time_since_detection = (
            datetime.now() - self.fall_detected_timestamp
        ).total_seconds()
        
        if time_since_detection >= self.fall_confirmation_delay_seconds:
            # Fall confirmed
            self.fall_detected_timestamp = None
            
            alert = self._create_alert(
                "FALL DETECTED",
                "A fall has been detected. Emergency services may be contacted. Confirm you're safe.",
                AlertSeverity.EMERGENCY,
                action_required=True,
                suggested_action="Press to confirm safety"
            )
            
            self._trigger_emergency_response(alert)
            return alert
        
        return None
    
    def _handle_scream_detection(self, sensor_data: SensorData) -> Optional[Alert]:
        """Handle scream detection"""
        # Check cooldown to avoid spam
        if self.scream_detected_timestamp:
            if (datetime.now() - self.scream_detected_timestamp).total_seconds() < self.alert_cooldown_seconds:
                return None
        
        self.scream_detected_timestamp = datetime.now()
        
        alert = self._create_alert(
            "Distress Detected",
            "A scream or distress signal was detected. Are you OK?",
            AlertSeverity.CRITICAL,
            action_required=True,
            suggested_action="Press to confirm safety"
        )
        
        self._trigger_emergency_response(alert)
        return alert
    
    def _is_user_actively_moving(self, sensor_data: SensorData) -> bool:
        """Check if abnormal motion is from user activity"""
        # This is a simplified check - in production would be more sophisticated
        # For example, detect if user is holding phone and intentionally moving it
        return False
    
    def _create_alert(self, title: str, message: str, severity: AlertSeverity,
                     action_required: bool = False,
                     suggested_action: Optional[str] = None) -> Alert:
        """Create a new alert"""
        alert = Alert(
            id=f"alert_{datetime.now().timestamp()}",
            severity=severity,
            title=title,
            message=message,
            timestamp=datetime.now(),
            action_required=action_required,
            suggested_action=suggested_action,
            dismissed=False
        )
        
        self.active_alerts.append(alert)
        return alert
    
    def _trigger_emergency_response(self, alert: Alert):
        """Trigger emergency response"""
        if not self.emergency_mode_active:
            self.emergency_mode_active = True
            
            if self.emergency_callback:
                self.emergency_callback(alert)
    
    def acknowledge_alert(self, alert_id: str, user_safe: bool = True):
        """User acknowledges an alert"""
        alert = next((a for a in self.active_alerts if a.id == alert_id), None)
        
        if alert:
            alert.dismissed = True
            
            if user_safe:
                self.emergency_mode_active = False
            else:
                # User indicates they're not safe - escalate
                self._escalate_emergency()
    
    def _escalate_emergency(self):
        """Escalate emergency - would contact services"""
        # In production, this would contact emergency services
        pass
    
    def cancel_fall_detection(self):
        """Cancel fall detection if user is OK"""
        self.fall_detected_timestamp = None
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all active (non-dismissed) alerts"""
        return [a for a in self.active_alerts if not a.dismissed]
    
    def get_alert_status(self) -> Dict[str, any]:
        """Get alert system status"""
        active = self.get_active_alerts()
        
        return {
            "emergency_mode_active": self.emergency_mode_active,
            "active_alerts_count": len(active),
            "critical_alerts": len([a for a in active if a.severity == AlertSeverity.EMERGENCY]),
            "emergency_contacts_set": len(self.emergency_contacts) > 0,
            "emergency_contacts": self.emergency_contacts,
            "alerts": [
                {
                    "id": a.id,
                    "title": a.title,
                    "severity": a.severity.value,
                    "timestamp": a.timestamp.isoformat()
                }
                for a in active
            ]
        }
