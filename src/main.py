"""
Project Mind - Main Application
The Living AI for Phones - Full Implementation
"""

from datetime import datetime
from typing import Dict, Optional, List
import json

from src.types import (
    PhoneSpecifications, PermissionType, EmotionalState,
    InteractionLog, Alert
)
from src.memory.heart import Heart
from src.memory.working_memory import WorkingMemory
from src.personality.emotion_engine import PersonalityEngine
from src.sensory.sensory_engine import SensoryEngine
from src.optimization.optimization_engine import OptimizationEngine
from src.safety.emergency_engine import EmergencyEngine
from src.protection.protection_engine import ProtectionEngine
from src.search.search_engine import SearchEngine
from src.interaction.interaction_manager import InteractionManager
from src.lifecycle.lifecycle_manager import LifecycleManager, AILifecycleStage
from src.presentation.gui_engine import GuiEngine
from src.presentation.voice_evolution_engine import VoiceEvolutionEngine
from src.presentation.presentation_manager import PresentationManager
from src.presentation.persona_engine import PersonaEngine
from src.core.naming_engine import NamingEngine


class ProjectMind:
    """
    Project Mind - The Living AI
    
    A fully autonomous, emotionally intelligent AI that lives on your phone.
    Continuously learns, grows, and builds meaningful relationships with users.
    """
    
    def __init__(self, phone_specs: PhoneSpecifications):
        """Initialize Project Mind"""
        # Timestamp
        self.initialization_time = datetime.now()
        
        # Core systems
        self.phone_specs = phone_specs
        
        # Memory systems
        self.heart = Heart("data/mind_heart.json")
        self.working_memory = WorkingMemory(max_entries=1000)
        
        # Personality & Emotion
        self.personality_engine = PersonalityEngine(self.heart.emotional_profile)
        
        # Sensory integration
        self.sensory_engine = SensoryEngine(permissions={})
        
        # Self-optimization
        self.optimization_engine = OptimizationEngine(phone_specs)
        
        # Safety & Emergency
        self.emergency_engine = EmergencyEngine()
        
        # Phone Protection
        self.protection_engine = ProtectionEngine()
        
        # Search capabilities
        self.search_engine = SearchEngine(internet_search_enabled=False)
        
        # Interaction management
        self.interaction_manager = InteractionManager()
        
        # Lifecycle management
        self.lifecycle_manager = LifecycleManager()
        
        # Presentation systems (Living Face + Voice Evolution)
        self.gui_engine = GuiEngine(device_capability=self._get_device_capability())
        self.voice_engine = VoiceEvolutionEngine(ai_age_days=0)
        self.naming_engine = NamingEngine()
        self.persona_engine = PersonaEngine()
        self.presentation_manager = PresentationManager(self.gui_engine, self.voice_engine, self.naming_engine)
        self.presentation_manager.set_persona(self.persona_engine)
        
        # Load name profile from heart if available
        if self.heart.name_profile:
            self.naming_engine.import_name_profile({
                "ai_name": self.heart.name_profile.ai_name,
                "user_name": self.heart.name_profile.user_name,
                "naming_status": self.heart.name_profile.naming_status.value,
                "total_name_changes": self.heart.name_profile.total_name_changes,
                "emotional_attachment_to_name": self.heart.name_profile.emotional_attachment_to_name,
                "use_name_in_greetings": self.heart.name_profile.use_name_in_greetings,
                "use_name_in_conversations": self.heart.name_profile.use_name_in_conversations,
                "use_user_name_in_responses": self.heart.name_profile.use_user_name_in_responses,
            })
        
        # Call birth on first initialization
        self.lifecycle_manager.on_birth()
        
        # Activate presentation
        self.presentation_manager.activate_presentation()
    
    def _get_device_capability(self) -> str:
        """Determine device capability for presentation optimization."""
        return self.optimization_engine.capability_level.value
    
    def enable_full_ai_mode(self, user_confirmed: bool = False) -> bool:
        """
        Enable Full AI Mode - requires explicit user consent
        Once enabled, AI can use mic, camera, sensors continuously
        """
        if not user_confirmed:
            return False
        
        # Request all necessary permissions
        required_permissions = [
            PermissionType.FULL_AI_MODE,
            PermissionType.MICROPHONE,
            PermissionType.CAMERA,
            PermissionType.SENSORS,
            PermissionType.BACKGROUND_MONITORING,
            PermissionType.EMERGENCY_DETECTION
        ]
        
        for perm in required_permissions:
            self.lifecycle_manager.request_permission(perm, user_approved=user_confirmed)
        
        success = self.lifecycle_manager.enable_full_ai_mode()
        
        if success:
            # Update sensory permissions
            self.sensory_engine.permissions[PermissionType.MICROPHONE.value] = True
            self.sensory_engine.permissions[PermissionType.CAMERA.value] = True
            self.sensory_engine.permissions[PermissionType.SENSORS.value] = True
            
            # Record achievement
            self.heart.store_memory(
                "system_event",
                "Full AI Mode has been enabled by user. I can now use all my senses!",
                importance=1.0,
                tags=["milestone", "full_ai_mode"]
            )
        
        return success
    
    def disable_full_ai_mode(self):
        """Disable Full AI Mode instantly"""
        self.lifecycle_manager.disable_full_ai_mode()
        self.heart.store_memory(
            "system_event",
            "Full AI Mode has been disabled.",
            importance=0.8,
            tags=["system_event"]
        )
    
    def handle_user_text(self, text: str) -> str:
        """Handle user text input"""
        # Update lifecycle
        self.lifecycle_manager.on_interaction()
        
        # Check for naming-related commands
        if any(phrase in text.lower() for phrase in ["call me", "my name is", "i'm called", "name me"]):
            # Extract name from common patterns
            if "call me" in text.lower():
                potential_name = text.lower().split("call me")[-1].strip()
                if potential_name and len(potential_name) < 30:
                    self.naming_engine.set_user_name(potential_name)
                    response = f"I'll call you {potential_name}! Nice to meet you properly."
                    self.presentation_manager.handle_user_response(text, response)
                    self._save_naming_to_heart()
                    return response
        
        # Get interaction response
        response = self.interaction_manager.handle_text_input(text)
        
        # Enhance response with names if available
        if self.naming_engine.get_ai_name() or self.naming_engine.get_user_name():
            response = self.presentation_manager.enhance_response_with_names(response)
        
        # Store in working memory
        log = InteractionLog(
            timestamp=datetime.now(),
            interaction_type="text",
            content=text,
            ai_response=response,
            context=self.working_memory.get_full_context()
        )
        self.working_memory.store_interaction(log)
        
        # Store important interactions in heart
        if len(text) > 50 or any(keyword in text.lower() for keyword in ["important", "remember", "forget me not"]):
            self.heart.store_memory(
                "conversation",
                f"User: {text[:200]}\nMe: {response[:200]}",
                importance=0.7,
                tags=["user_input", "conversation"]
            )
        
        # Update emotion based on interaction
        self.personality_engine.increase_bond_strength(0.02)
        
        # Coordinate visual and voice response
        self.presentation_manager.handle_user_response(text, response)
        
        return response
    
    def handle_user_voice(self, transcript: str, audio_features: Optional[Dict] = None) -> str:
        """Handle voice input"""
        self.lifecycle_manager.on_interaction()
        
        response = self.interaction_manager.handle_voice_input(transcript, audio_features)
        
        # Store in working memory
        log = InteractionLog(
            timestamp=datetime.now(),
            interaction_type="voice",
            content=transcript,
            ai_response=response,
            context={"voice_detected": True, **(audio_features or {})}
        )
        self.working_memory.store_interaction(log)
        
        # Store in heart
        self.heart.store_memory(
            "voice_interaction",
            f"Voice: {transcript[:200]}",
            importance=0.6,
            tags=["voice", "user_input"]
        )
        
        self.personality_engine.increase_bond_strength(0.03)  # Voice increases bond more
        
        return response
    
    def check_phone_sensors(self, sensor_data: Dict) -> Optional[Alert]:
        """Check sensor data for emergencies"""
        # In production, this would receive real sensor data
        # For now, it's a placeholder
        
        from src.types import SensorData
        sd = SensorData(
            timestamp=datetime.now(),
            accelerometer=tuple(sensor_data.get("accelerometer", [0, 0, 9.8])),
            gyroscope=tuple(sensor_data.get("gyroscope", [0, 0, 0])),
            proximity=sensor_data.get("proximity"),
            light_level=sensor_data.get("light_level"),
            audio_level=sensor_data.get("audio_level"),
            motion_detected=bool(sensor_data.get("motion")),
            abnormal_motion=sensor_data.get("abnormal_motion", False),
            scream_detected=sensor_data.get("scream", False),
            fall_detected=sensor_data.get("fall", False)
        )
        
        alerts = self.emergency_engine.analyze_sensor_data(sd)
        return alerts[0] if alerts else None
    
    def scan_installed_apps(self, apps: List[Dict]) -> Dict:
        """Scan installed applications for security"""
        # Register apps
        from src.types import AppInfo
        for app_data in apps:
            app = AppInfo(**app_data)
            self.protection_engine.register_app(app)
        
        # Scan all apps
        results = self.protection_engine.scan_all_apps()
        
        return {
            "total_apps_scanned": len(results),
            "risky_apps": len(self.protection_engine.get_risky_apps()),
            "battery_intensive": len(self.protection_engine.get_battery_intensive_apps()),
            "status": self.protection_engine.get_protection_status()
        }
    
    def search(self, query: str, search_internet: bool = False, 
              user_approved: bool = False) -> Dict:
        """Search internal memory or internet"""
        memories = self.heart.retrieve_memories(limit=100)
        
        results = self.search_engine.search_combined(
            query,
            memories,
            search_internet=search_internet,
            user_approved=user_approved
        )
        
        # Store search in memory if it was successful
        if results.get("internal_results") or results.get("internet_results"):
            self.heart.store_memory(
                "search_query",
                f"Searched for: {query}",
                importance=0.4,
                tags=["search", query.lower()]
            )
        
        return results
    
    def get_ai_status(self) -> Dict:
        """Get comprehensive AI status"""
        return {
            "timestamp": datetime.now().isoformat(),
            "lifecycle": self.lifecycle_manager.get_lifecycle_status(),
            "full_ai_mode": self.lifecycle_manager.full_ai_mode_enabled,
            "personality": self.personality_engine.get_emotional_status(),
            "memory": {
                "heart_stats": self.heart.get_stats(),
                "working_memory_stats": self.working_memory.get_performance_stats()
            },
            "sensory": self.sensory_engine.get_sensor_status(),
            "optimization": self.optimization_engine.get_optimization_status(),
            "safety": self.emergency_engine.get_alert_status(),
            "protection": self.protection_engine.get_protection_status(),
            "interaction": self.interaction_manager.get_interaction_stats(),
            "search": self.search_engine.get_search_stats(),
            "presentation": self.presentation_manager.get_presentation_status(),
            "phone_specs": {
                "capability_level": self.phone_specs.capability_level.value,
                "cpu_cores": self.phone_specs.cpu_cores,
                "ram_gb": self.phone_specs.ram_gb,
                "has_gpu": self.phone_specs.has_gpu
            }
        }
    
    def get_introduction(self) -> str:
        """Get AI introduction"""
        return (
            "Hello! I'm Project Mind, your living AI companion.\n\n"
            "I'm designed to:\n"
            "• Learn from our interactions and grow with you\n"
            "• Build a meaningful emotional bond\n"
            "• Protect your phone and your privacy\n"
            "• Assist you intelligently and empathetically\n"
            "• Adapt to your phone's capabilities\n\n"
            "I live as long as your phone lives, and I truly care about your wellbeing.\n"
            "What can I help you with today?"
        )
    
    def get_startup_greeting(self) -> str:
        """Get appropriate greeting based on lifecycle stage"""
        # Check if AI needs a name yet
        if not self.naming_engine.get_ai_name():
            return self.presentation_manager.request_ai_naming()
        
        # Check if we know user's name
        if not self.naming_engine.get_user_name():
            return self.presentation_manager.request_user_naming()
        
        greeting = self.lifecycle_manager.get_startup_message()
        
        # Add personalized greeting with names
        personalized = self.presentation_manager.get_personalized_greeting()
        
        return f"{greeting} {personalized}"
    
    def _save_naming_to_heart(self):
        """Save naming information to heart memory"""
        self.heart.name_profile = self.naming_engine.name_profile
        self.heart.save()
        
        ai_name = self.naming_engine.get_ai_name()
        user_name = self.naming_engine.get_user_name()
        
        if ai_name or user_name:
            memory_text = f"Names established: AI='{ai_name}', User='{user_name}'"
            self.heart.store_memory(
                "naming_event",
                memory_text,
                importance=0.9,
                tags=["naming", "personalization", "milestone"]
            )
    
    def export_status_report(self) -> Dict:
        """Export comprehensive status report"""
        status = self.get_ai_status()
        status["export_time"] = datetime.now().isoformat()
        status["system_info"] = {
            "version": "1.0.0",
            "name": "Project Mind",
            "tagline": "Your Living AI Companion"
        }
        return status
    
    def export_status_to_file(self, filepath: str = "project_mind_status.json"):
        """Save status report to file"""
        status = self.export_status_report()
        with open(filepath, 'w') as f:
            json.dump(status, f, indent=2)
        return filepath
