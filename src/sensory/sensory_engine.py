"""
Sensory Integration Module
Manages microphone, camera, and sensor inputs
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple
import math
from src.types import SensorData


class SensoryEngine:
    """
    Manages all sensory inputs: microphone, camera, and phone sensors.
    Interprets and analyzes sensory data for AI decision-making.
    """
    
    def __init__(self, permissions: Dict[str, bool]):
        self.permissions = permissions
        
        # Current sensor states
        self.accelerometer_data: Optional[Tuple[float, float, float]] = None
        self.gyroscope_data: Optional[Tuple[float, float, float]] = None
        self.proximity_sensor: Optional[float] = None
        self.light_sensor: Optional[float] = None
        self.audio_level: Optional[float] = None
        
        # Sensor history for analysis
        self.motion_history: List[Tuple[datetime, Tuple[float, float, float]]] = []
        self.audio_history: List[Tuple[datetime, float]] = []
        
        # Thresholds for detection
        self.fall_detection_threshold = 2.5  # g force
        self.scream_detection_threshold = 85  # dB
        self.abnormal_motion_threshold = 3.0  # g force
    
    def is_microphone_enabled(self) -> bool:
        """Check if microphone is enabled"""
        return self.permissions.get("microphone", False)
    
    def is_camera_enabled(self) -> bool:
        """Check if camera is enabled"""
        return self.permissions.get("camera", False)
    
    def is_sensors_enabled(self) -> bool:
        """Check if sensors are enabled"""
        return self.permissions.get("sensors", False)
    
    def update_motion(self, accel: Tuple[float, float, float], 
                     gyro: Tuple[float, float, float]):
        """Update motion sensor data"""
        if not self.is_sensors_enabled():
            return
        
        self.accelerometer_data = accel
        self.gyroscope_data = gyro
        
        # Record for history
        self.motion_history.append((datetime.now(), accel))
        
        # Keep only last 100 readings
        if len(self.motion_history) > 100:
            self.motion_history = self.motion_history[-100:]
    
    def update_audio_level(self, level_db: float):
        """Update audio level"""
        if not self.is_microphone_enabled():
            return
        
        self.audio_level = level_db
        self.audio_history.append((datetime.now(), level_db))
        
        # Keep only last 100 readings
        if len(self.audio_history) > 100:
            self.audio_history = self.audio_history[-100:]
    
    def update_proximity(self, distance_cm: float):
        """Update proximity sensor"""
        if not self.is_sensors_enabled():
            return
        self.proximity_sensor = distance_cm
    
    def update_light_level(self, lux: float):
        """Update ambient light level"""
        if not self.is_sensors_enabled():
            return
        self.light_sensor = lux
    
    def detect_fall(self) -> bool:
        """Detect if user has fallen"""
        if not self.is_sensors_enabled() or not self.accelerometer_data:
            return False
        
        # Calculate total acceleration (magnitude)
        ax, ay, az = self.accelerometer_data
        total_accel = math.sqrt(ax**2 + ay**2 + az**2)
        
        # Check for sudden drop (fall characteristic)
        if len(self.motion_history) > 10:
            recent = [mag for _, (x, y, z) in self.motion_history[-10:] 
                     for mag in [math.sqrt(x**2 + y**2 + z**2)]]
            avg_recent = sum(recent) / len(recent)
            
            # Fall detected if sudden acceleration spike followed by drop
            if total_accel > self.fall_detection_threshold and avg_recent < 1.0:
                return True
        
        return False
    
    def detect_scream(self) -> bool:
        """Detect scream or loud cry"""
        if not self.is_microphone_enabled() or not self.audio_level:
            return False
        
        return self.audio_level > self.scream_detection_threshold
    
    def detect_abnormal_motion(self) -> bool:
        """Detect abnormal motion patterns"""
        if not self.is_sensors_enabled():
            return False
        
        if not self.accelerometer_data:
            return False
        
        ax, ay, az = self.accelerometer_data
        total_accel = math.sqrt(ax**2 + ay**2 + az**2)
        
        # High acceleration is abnormal
        return total_accel > self.abnormal_motion_threshold
    
    def get_environment_brightness(self) -> str:
        """Get environment brightness level"""
        if not self.is_sensors_enabled() or self.light_sensor is None:
            return "unknown"
        
        if self.light_sensor < 50:
            return "very_dark"
        elif self.light_sensor < 500:
            return "dark"
        elif self.light_sensor < 2000:
            return "dim"
        elif self.light_sensor < 10000:
            return "normal"
        else:
            return "bright"
    
    def is_device_in_hand(self) -> bool:
        """Check if device is being held"""
        if not self.is_sensors_enabled():
            return False
        
        # Proximity sensor: device is in hand if proximity < 5cm
        if self.proximity_sensor is not None:
            return self.proximity_sensor < 5.0
        
        return False
    
    def get_motion_stability(self) -> float:
        """Get motion stability (0.0 = unstable, 1.0 = very stable)"""
        if not self.is_sensors_enabled() or not self.motion_history:
            return 0.5
        
        # Calculate variance in recent motion
        recent = [math.sqrt(x**2 + y**2 + z**2) 
                 for _, (x, y, z) in self.motion_history[-20:]]
        
        if not recent:
            return 0.5
        
        avg_accel = sum(recent) / len(recent)
        variance = sum((x - avg_accel) ** 2 for x in recent) / len(recent)
        
        # Convert to stability score (lower variance = higher stability)
        stability = 1.0 - min(1.0, variance / 10.0)
        return stability
    
    def get_sensor_data_snapshot(self) -> SensorData:
        """Get current sensor state snapshot"""
        return SensorData(
            timestamp=datetime.now(),
            accelerometer=self.accelerometer_data,
            gyroscope=self.gyroscope_data,
            proximity=self.proximity_sensor,
            light_level=self.light_sensor,
            audio_level=self.audio_level,
            motion_detected=bool(self.accelerometer_data),
            abnormal_motion=self.detect_abnormal_motion(),
            scream_detected=self.detect_scream(),
            fall_detected=self.detect_fall()
        )
    
    def get_sensor_status(self) -> Dict[str, any]:
        """Get comprehensive sensor status"""
        return {
            "microphone_enabled": self.is_microphone_enabled(),
            "camera_enabled": self.is_camera_enabled(),
            "sensors_enabled": self.is_sensors_enabled(),
            "audio_level_db": self.audio_level,
            "light_level_lux": self.light_sensor,
            "proximity_cm": self.proximity_sensor,
            "environment_brightness": self.get_environment_brightness(),
            "device_in_hand": self.is_device_in_hand(),
            "motion_stability": self.get_motion_stability(),
            "fall_detected": self.detect_fall(),
            "scream_detected": self.detect_scream(),
            "abnormal_motion": self.detect_abnormal_motion()
        }
