"""
Project Mind - Presentation Integration
Synchronizes the GUI Face and Voice Evolution systems to create a unified,
expressive AI presence that looks and sounds alive.

This module ensures:
- Facial expressions match voice tone
- Voice timing synchronizes with mouth animations
- Emotions are expressed visually and aurally
- User preferences apply to both systems
- Resource optimization across both engines
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime

from src.types import (
    EmotionalState, ExpressionIntensity, FacialExpression,
    FacePreferences, VoicePreferences, NameProfile, PersonaProfile
)


class PresentationManager:
    """
    Coordinates the GUI Face Engine and Voice Evolution Engine
    to create a cohesive, expressive AI presence.
    
    Features:
    - Synchronized facial expressions with voice synthesis
    - Emotion-driven changes to appearance and voice
    - User customization of both visual and audio aspects
    - Memory integration for persistent preferences
    - Resource optimization for different device capabilities
    """
    
    def __init__(self, gui_engine=None, voice_engine=None, naming_engine=None):
        """
        Initialize the Presentation Manager.
        
        Args:
            gui_engine: GuiEngine instance
            voice_engine: VoiceEvolutionEngine instance
            naming_engine: NamingEngine instance for personalization
        """
        self.gui_engine = gui_engine
        self.voice_engine = voice_engine
        self.naming_engine = naming_engine
        self.persona_engine = None
        
        self.is_active = False
        self.last_sync_time = None
        self.emotion_history: List[tuple] = []
        self.interaction_count = 0
        
        # Preference sync
        self.shared_preferences = {
            "enable_living_presence": True,
            "emotion_expression_intensity": ExpressionIntensity.MODERATE,
            "response_animation": True,
            "voice_sync": True,
            "use_personalized_names": True
        }
    
    def activate_presentation(self) -> None:
        """Activate the living presence (face + voice systems)."""
        self.is_active = True
        if self.gui_engine:
            self.gui_engine.set_visibility(True, mode="widget")
    
    def deactivate_presentation(self) -> None:
        """Deactivate the living presence."""
        self.is_active = False
        if self.gui_engine:
            self.gui_engine.set_visibility(False)
        if self.voice_engine:
            self.voice_engine.stop_speech()
    
    def update_emotion_expression(self, emotion: EmotionalState) -> None:
        """
        Update both face and voice to express the given emotion.
        
        Args:
            emotion: EmotionalState to express
        """
        if not self.is_active:
            return
        
        # Log emotion
        self.emotion_history.append((emotion, datetime.now()))
        
        # Update facial expression
        if self.gui_engine:
            intensity = self.shared_preferences["emotion_expression_intensity"]
            self.gui_engine.update_facial_expression(emotion, intensity)
        
        # Update voice modulation
        if self.voice_engine:
            self.voice_engine.update_emotion(emotion)
        
        self.last_sync_time = datetime.now()
    
    def handle_user_response(self, user_input: str, ai_response: str) -> Dict[str, Any]:
        """
        Coordinate facial and voice response to user input.
        
        Args:
            user_input: User's input text
            ai_response: AI's response text
        
        Returns:
            Dictionary with response details
        """
        self.interaction_count += 1
        
        response_data = {
            "interaction_id": f"interaction_{self.interaction_count}",
            "gui_sync": None,
            "voice_sync": None,
            "timestamp": datetime.now().isoformat()
        }
        
        if not self.is_active:
            return response_data
        
        # Analyze sentiment to determine appropriate expression
        # (In real implementation, would use NLP)
        if "happy" in ai_response.lower() or "great" in ai_response.lower():
            response_emotion = EmotionalState.HAPPY
        elif "concerned" in ai_response.lower() or "worried" in ai_response.lower():
            response_emotion = EmotionalState.CONCERNED
        elif "curious" in ai_response.lower() or "?" in ai_response:
            response_emotion = EmotionalState.CURIOUS
        else:
            response_emotion = EmotionalState.CALM
        
        # Update emotion expression
        self.update_emotion_expression(response_emotion)
        
        # Generate voice and synchronized facial animation
        if self.gui_engine and self.voice_engine:
            # Map emotion to facial expression
            emotion_to_expression = {
                EmotionalState.HAPPY: FacialExpression.HAPPY,
                EmotionalState.CURIOUS: FacialExpression.CURIOUS,
                EmotionalState.CONCERNED: FacialExpression.CONCERNED,
                EmotionalState.EXCITED: FacialExpression.EXCITED,
                EmotionalState.CALM: FacialExpression.LISTENING,
                EmotionalState.FOCUSED: FacialExpression.THINKING,
                EmotionalState.PLAYFUL: FacialExpression.SMILE,
                EmotionalState.PROTECTIVE: FacialExpression.CONCERNED
            }
            
            facial_expr = emotion_to_expression.get(response_emotion, FacialExpression.NEUTRAL)
            
            # Generate synchronized speech event
            sync_event = self.voice_engine.synthesize_speech(ai_response, facial_expr)
            response_data["voice_sync"] = {
                "event_id": sync_event.event_id,
                "text": ai_response,
                "duration_ms": sync_event.duration_ms,
                "pitch": sync_event.voice_pitch,
                "speed": sync_event.voice_speed,
                "facial_expression": sync_event.facial_expression.value
            }
            
            # Sync facial animation
            self.gui_engine.sync_with_speech(ai_response, sync_event.duration_ms)
            response_data["gui_sync"] = {
                "expression": facial_expr.value,
                "duration_ms": sync_event.duration_ms,
                "is_speaking": True
            }
        
        return response_data
    
    def sync_preferences(self, face_prefs: Optional[FacePreferences] = None,
                        voice_prefs: Optional[VoicePreferences] = None) -> None:
        """
        Synchronize preferences across both engines.
        
        Args:
            face_prefs: FacePreferences object
            voice_prefs: VoicePreferences object
        """
        if face_prefs and self.gui_engine:
            self.gui_engine.set_face_preferences(face_prefs)
        
        if voice_prefs and self.voice_engine:
            self.voice_engine.set_voice_preferences(voice_prefs)
        
        self.last_sync_time = datetime.now()
    
    def handle_gesture(self, gesture_type: str) -> None:
        """
        Handle user gestures and respond with appropriate expressions.
        
        Args:
            gesture_type: Type of gesture (e.g., "tap", "shake", "swipe")
        """
        if not self.is_active or not self.gui_engine:
            return
        
        if gesture_type == "tap":
            self.gui_engine.handle_nod()
            self.update_emotion_expression(EmotionalState.CURIOUS)
        elif gesture_type == "shake":
            self.gui_engine.animate_expression(FacialExpression.EXCITED)
            self.update_emotion_expression(EmotionalState.EXCITED)
        elif gesture_type == "swipe":
            self.gui_engine.animate_expression(FacialExpression.HAPPY)
            self.update_emotion_expression(EmotionalState.PLAYFUL)
    
    def update_battery_status(self, battery_percent: int) -> None:
        """
        Adapt presentation quality based on battery level.
        
        Args:
            battery_percent: Current battery percentage
        """
        if self.gui_engine:
            self.gui_engine.optimize_for_battery(battery_percent)
        
        # Voice TTS could also be optimized here if needed
    
    def update_ai_age(self, age_days: int) -> None:
        """
        Update presentation for AI age/maturation.
        
        Args:
            age_days: AI age in days
        """
        if self.voice_engine:
            self.voice_engine.update_age(age_days)
    
    def get_presentation_status(self) -> Dict[str, Any]:
        """
        Get complete presentation status including both GUI and voice.
        
        Returns:
            Dictionary with all presentation information
        """
        status = {
            "is_active": self.is_active,
            "interaction_count": self.interaction_count,
            "last_sync": self.last_sync_time.isoformat() if self.last_sync_time else None,
            "shared_preferences": {
                k: v.value if hasattr(v, 'value') else v
                for k, v in self.shared_preferences.items()
            }
        }
        
        if self.gui_engine:
            status["gui"] = self.gui_engine.get_gui_status()
        
        if self.voice_engine:
            status["voice"] = self.voice_engine.get_voice_evolution_status()
        
        return status
    
    def render_complete_response(self, 
                                response_text: str,
                                emotional_context: EmotionalState) -> Dict[str, Any]:
        """
        Render a complete response with coordinated visual and audio output.
        
        Args:
            response_text: Text to output
            emotional_context: Emotional context of the response
        
        Returns:
            Complete rendering specification
        """
        if not self.is_active:
            return {"error": "Presentation not active"}
        
        render_spec = {
            "timestamp": datetime.now().isoformat(),
            "emotion": emotional_context.value,
            "gui_frame": None,
            "voice_params": None
        }
        
        if self.gui_engine:
            self.gui_engine.update_facial_expression(emotional_context)
            render_spec["gui_frame"] = self.gui_engine.render_frame()
        
        if self.voice_engine:
            self.voice_engine.update_emotion(emotional_context)
            render_spec["voice_params"] = self.voice_engine.get_voice_parameters()
        
        return render_spec
    
    def get_emotion_trends(self, hours: int = 24) -> Dict[str, int]:
        """
        Get trends of emotions expressed in the given time period.
        
        Args:
            hours: Number of hours to analyze
        
        Returns:
            Dictionary of emotion frequencies
        """
        cutoff_time = datetime.now() - __import__('datetime').timedelta(hours=hours)
        
        trends = {}
        for emotion, timestamp in self.emotion_history:
            if timestamp >= cutoff_time:
                emotion_key = emotion.value
                trends[emotion_key] = trends.get(emotion_key, 0) + 1
        
        return trends
    
    def export_presentation_profile(self) -> Dict[str, Any]:
        """
        Export complete presentation profile for persistence.
        
        Returns:
            Dictionary with all presentation settings
        """
        profile = {
            "created_at": datetime.now().isoformat(),
            "shared_settings": self.shared_preferences,
            "interaction_history": {
                "total_interactions": self.interaction_count,
                "emotion_distribution": self.get_emotion_trends(hours=168)  # Last week
            }
        }
        
        if self.gui_engine:
            profile["face_settings"] = {
                "style": self.gui_engine.face_preferences.style.value,
                "skin_tone": self.gui_engine.face_preferences.skin_tone.value,
                "expression_intensity": self.gui_engine.face_preferences.expression_intensity.value,
                "eye_color": self.gui_engine.face_preferences.eye_color
            }
        
        if self.voice_engine:
            profile["voice_settings"] = {
                "gender": self.voice_engine.voice_preferences.gender.value,
                "base_tone": self.voice_engine.voice_preferences.base_tone.value,
                "pitch_offset": self.voice_engine.voice_preferences.pitch_offset,
                "speed_offset": self.voice_engine.voice_preferences.speed_offset,
                "volume": self.voice_engine.voice_preferences.volume_level
            }
        
        if self.naming_engine:
            profile["naming_settings"] = self.naming_engine.export_name_profile()
        
        return profile
    
    # ============================================================
    # NAMING SYSTEM INTEGRATION
    # ============================================================
    
    def get_personalized_greeting(self) -> str:
        """
        Get a personalized greeting using AI and user names.
        
        Returns:
            Personalized greeting string
        """
        if not self.naming_engine or not self.shared_preferences.get("use_personalized_names"):
            return "Hello! How can I help you?"
        
        current_emotion = self.emotion_history[-1][0] if self.emotion_history else EmotionalState.CURIOUS
        return self.naming_engine.get_greeting(current_emotion)
    
    def enhance_response_with_names(self, response: str, template_type: str = "acknowledgment") -> str:
        """
        Enhance a response with personalized names.
        
        Args:
            response: Original response text
            template_type: Type of response template
        
        Returns:
            Enhanced response with names
        """
        if not self.naming_engine or not self.shared_preferences.get("use_personalized_names"):
            return response
        
        return self.naming_engine.enhance_response(response, template_type)
    
    def request_ai_naming(self) -> str:
        """
        Get prompt to request AI name from user.
        
        Returns:
            Naming request prompt
        """
        if not self.naming_engine:
            return ""
        return self.naming_engine.request_ai_name_from_user()
    
    def request_user_naming(self) -> str:
        """
        Get prompt to request user name.
        
        Returns:
            User naming request prompt
        """
        if not self.naming_engine:
            return ""
        return self.naming_engine.request_user_name_from_user()
    
    def set_ai_name(self, name: str) -> bool:
        """
        Set AI name through presentation system.
        
        Args:
            name: AI name to set
        
        Returns:
            True if name was set successfully
        """
        if not self.naming_engine:
            return False
        return self.naming_engine.set_ai_name(name)
    
    def set_user_name(self, name: str) -> bool:
        """
        Set user name through presentation system.
        
        Args:
            name: User name to set
        
        Returns:
            True if name was set successfully
        """
        if not self.naming_engine:
            return False
        return self.naming_engine.set_user_name(name)
    
    def get_ai_name(self) -> Optional[str]:
        """Get AI's current name."""
        if not self.naming_engine:
            return None
        return self.naming_engine.get_ai_name()
    
    def get_user_name(self) -> Optional[str]:
        """Get remembered user name."""
        if not self.naming_engine:
            return None
        return self.naming_engine.get_user_name()
    
    def get_naming_status(self) -> Dict[str, Any]:
        """
        Get complete naming status.
        
        Returns:
            Dictionary with naming information
        """
        if not self.naming_engine:
            return {"status": "naming_disabled"}
        
        return self.naming_engine.get_naming_status_summary()
    
    def set_persona(self, persona_engine) -> bool:
        """Set persona engine reference"""
        self.persona_engine = persona_engine
        return True
    
    def apply_persona_to_output(self, base_response: str) -> str:
        """Apply persona communication style to response"""
        if not self.persona_engine:
            return base_response
        
        behavior = self.persona_engine.current_behavior
        if not behavior:
            return base_response
        
        adjusted = base_response
        
        if behavior.communication_style:
            if behavior.communication_style == "formal":
                adjusted = adjusted.rstrip("!?.")
                adjusted += "."
            elif behavior.communication_style == "casual":
                if not adjusted.endswith(("!", "?")):
                    adjusted = adjusted.rstrip(".") + "!"
        
        return adjusted
    
    def get_persona_status(self) -> Optional[Dict[str, Any]]:
        """Get current persona status"""
        if not self.persona_engine:
            return None
        return self.persona_engine.get_persona_status()
