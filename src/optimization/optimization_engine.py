"""
Self-Optimization Engine Module
Detects hardware specs and dynamically adjusts AI modules
"""

from typing import Dict, List, Optional
from src.types import PhoneSpecifications, PhoneSpecLevel, ContextProfile


class OptimizationEngine:
    """
    The Optimization Engine detects phone hardware and self-tunes the AI.
    Adjusts processing, memory usage, and module activation based on device capability.
    """
    
    def __init__(self, phone_specs: PhoneSpecifications):
        self.phone_specs = phone_specs
        self.capability_level = phone_specs.capability_level
        
        # Performance profiles
        self.current_profile = ContextProfile.AFTERNOON
        self.performance_profiles = self._init_profiles()
        
        # Active modules based on capability
        self.active_modules = self._determine_active_modules()
        
        # Resource limits
        self.max_background_processes = self._calculate_max_processes()
        self.memory_limit_mb = self._calculate_memory_limit()
        self.processing_speed_factor = self._calculate_speed_factor()
    
    def _init_profiles(self) -> Dict[ContextProfile, Dict[str, any]]:
        """Initialize performance profiles for different contexts"""
        return {
            ContextProfile.MORNING: {
                "processing_priority": "normal",
                "background_tasks": 3,
                "learning_enabled": True,
                "vision_enabled": True,
            },
            ContextProfile.AFTERNOON: {
                "processing_priority": "normal",
                "background_tasks": 5,
                "learning_enabled": True,
                "vision_enabled": True,
            },
            ContextProfile.NIGHT: {
                "processing_priority": "low",
                "background_tasks": 2,
                "learning_enabled": False,
                "vision_enabled": False,
            },
            ContextProfile.GAMING: {
                "processing_priority": "low",
                "background_tasks": 1,
                "learning_enabled": False,
                "vision_enabled": False,
            },
            ContextProfile.CHARGING: {
                "processing_priority": "high",
                "background_tasks": 10,
                "learning_enabled": True,
                "vision_enabled": True,
            },
            ContextProfile.LOW_BATTERY: {
                "processing_priority": "minimal",
                "background_tasks": 0,
                "learning_enabled": False,
                "vision_enabled": False,
            },
            ContextProfile.WORK: {
                "processing_priority": "high",
                "background_tasks": 4,
                "learning_enabled": True,
                "vision_enabled": True,
            },
            ContextProfile.SOCIAL: {
                "processing_priority": "normal",
                "background_tasks": 6,
                "learning_enabled": True,
                "vision_enabled": True,
            },
        }
    
    def _determine_active_modules(self) -> Dict[str, bool]:
        """Determine which modules should be active based on hardware"""
        modules = {
            "core_ai": True,  # Always active
            "emotion_engine": True,  # Always active
            "memory": True,  # Always active
            "sensory_basic": True,  # Always active (basic touch/mic)
        }
        
        # Vision requires camera
        modules["vision"] = self.phone_specs.has_camera
        
        # Advanced vision requires good GPU
        modules["advanced_vision"] = (
            self.phone_specs.has_camera and 
            self.phone_specs.has_gpu and
            self.capability_level != PhoneSpecLevel.LOW_END
        )
        
        # Optimization engine always active
        modules["optimization"] = True
        
        # Emergency detection based on sensors
        modules["emergency_detection"] = (
            self.phone_specs.has_accelerometer or
            self.phone_specs.has_microphone
        )
        
        # Background processing on better devices
        modules["background_processing"] = (
            self.capability_level != PhoneSpecLevel.LOW_END
        )
        
        # Cloud sync on capable devices
        modules["cloud_sync"] = (
            self.capability_level == PhoneSpecLevel.HIGH_END
        )
        
        return modules
    
    def _calculate_max_processes(self) -> int:
        """Calculate maximum background processes"""
        base = {
            PhoneSpecLevel.LOW_END: 2,
            PhoneSpecLevel.MID_RANGE: 5,
            PhoneSpecLevel.HIGH_END: 10,
        }
        return base[self.capability_level]
    
    def _calculate_memory_limit(self) -> int:
        """Calculate working memory limit in MB"""
        # Use a fraction of available RAM
        fraction = {
            PhoneSpecLevel.LOW_END: 0.15,
            PhoneSpecLevel.MID_RANGE: 0.25,
            PhoneSpecLevel.HIGH_END: 0.35,
        }
        
        limit_mb = int(self.phone_specs.ram_gb * 1024 * fraction[self.capability_level])
        return max(128, limit_mb)  # Minimum 128MB
    
    def _calculate_speed_factor(self) -> float:
        """Calculate processing speed factor"""
        # Normalize to CPU cores and frequency
        base_score = self.phone_specs.cpu_cores * self.phone_specs.cpu_frequency_ghz
        
        if base_score < 5:
            return 0.5  # Low-end: slower processing
        elif base_score < 15:
            return 1.0  # Mid-range: normal processing
        else:
            return 1.5  # High-end: faster processing
    
    def switch_profile(self, profile: ContextProfile):
        """Switch to a different performance profile"""
        if profile in self.performance_profiles:
            self.current_profile = profile
            return self.performance_profiles[profile]
        return None
    
    def set_context(self, hour: int, is_charging: bool, battery_percent: float,
                   app_in_foreground: Optional[str] = None):
        """Set system context to determine optimal profile"""
        # Time-based profile
        if hour < 6:
            new_profile = ContextProfile.NIGHT
        elif hour < 12:
            new_profile = ContextProfile.MORNING
        elif hour < 18:
            new_profile = ContextProfile.AFTERNOON
        else:
            new_profile = ContextProfile.NIGHT
        
        # Charging overrides time
        if is_charging:
            new_profile = ContextProfile.CHARGING
        
        # Low battery overrides
        elif battery_percent < 15:
            new_profile = ContextProfile.LOW_BATTERY
        
        # Gaming app
        elif app_in_foreground and "game" in app_in_foreground.lower():
            new_profile = ContextProfile.GAMING
        
        # Work context
        elif app_in_foreground and any(
            keyword in app_in_foreground.lower() 
            for keyword in ["office", "slack", "mail", "work", "teams"]
        ):
            new_profile = ContextProfile.WORK
        
        # Social context
        elif app_in_foreground and any(
            keyword in app_in_foreground.lower()
            for keyword in ["social", "tiktok", "instagram", "whatsapp"]
        ):
            new_profile = ContextProfile.SOCIAL
        
        self.current_profile = new_profile
    
    def get_current_profile_settings(self) -> Dict[str, any]:
        """Get current profile settings"""
        return self.performance_profiles[self.current_profile]
    
    def should_enable_vision(self) -> bool:
        """Check if vision processing should be enabled"""
        if not self.active_modules.get("vision"):
            return False
        
        profile = self.get_current_profile_settings()
        return profile.get("vision_enabled", False)
    
    def should_enable_learning(self) -> bool:
        """Check if learning/memory update should be enabled"""
        profile = self.get_current_profile_settings()
        return profile.get("learning_enabled", False)
    
    def get_max_inference_time_ms(self) -> int:
        """Get maximum time allowed for AI inference"""
        base = {
            PhoneSpecLevel.LOW_END: 500,
            PhoneSpecLevel.MID_RANGE: 300,
            PhoneSpecLevel.HIGH_END: 150,
        }
        return base[self.capability_level]
    
    def get_model_size_variant(self) -> str:
        """Get LLM model variant based on hardware"""
        return {
            PhoneSpecLevel.LOW_END: "mini",
            PhoneSpecLevel.MID_RANGE: "small",
            PhoneSpecLevel.HIGH_END: "base",
        }[self.capability_level]
    
    def get_optimization_status(self) -> Dict[str, any]:
        """Get current optimization status"""
        return {
            "device_capability": self.capability_level.value,
            "current_profile": self.current_profile.value,
            "active_modules": self.active_modules,
            "profile_settings": self.get_current_profile_settings(),
            "memory_limit_mb": self.memory_limit_mb,
            "max_background_processes": self.max_background_processes,
            "processing_speed_factor": self.processing_speed_factor,
            "model_variant": self.get_model_size_variant(),
            "max_inference_ms": self.get_max_inference_time_ms(),
        }
    
    def optimize_for_scenario(self, scenario: str) -> Dict[str, any]:
        """Optimize AI for specific scenario"""
        optimizations = {
            "quick_response": {
                "reduce_reasoning": True,
                "use_cached_responses": True,
                "parallel_processing": False,
            },
            "accuracy": {
                "reduce_reasoning": False,
                "use_cached_responses": False,
                "parallel_processing": True,
            },
            "energy_efficient": {
                "reduce_reasoning": True,
                "use_cached_responses": True,
                "background_learning": False,
            },
        }
        
        return optimizations.get(scenario, {})
