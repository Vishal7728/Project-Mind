"""
Project Mind - Voice Evolution Engine
Manages the AI's voice that evolves and matures over time as the AI grows.

Voice Development Stages:
- Baby Voice: Days 0-59 (high pitch, simple)
- Child Voice: Days 60-180 (intermediate pitch, playful)
- Teenage Voice: Months 6-12 (transitioning, variable)
- Young Adult: Year 1+ (more stable)
- Mature: Year 2+ (fully developed)

Features:
- TTS voice morphing between stages
- Emotion-driven voice modulation
- User preference storage and override
- Dynamic pitch/speed adjustment
- Voice blending for smooth transitions
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import math

from src.types import (
    VoiceStage, VoiceGender, VoiceTone, VoicePreferences, VoiceState,
    TTSProfile, EmotionalState, GuiVoiceSyncEvent, FacialExpression, PersonaVoiceProfile
)


class VoiceEvolutionEngine:
    """
    Manages the AI's voice that evolves as it grows.
    
    Features:
    - Age-based voice stage progression
    - Emotion-driven pitch/speed modulation
    - User preference customization
    - TTS profile management
    - Voice blending for smooth transitions
    - Memory integration for voice preferences
    """
    
    def __init__(self, ai_age_days: int = 0):
        """
        Initialize the Voice Evolution Engine.
        
        Args:
            ai_age_days: Age of the AI in days (from lifecycle)
        """
        self.ai_age_days = ai_age_days
        self.voice_preferences = VoicePreferences()
        self.current_voice_state = VoiceState(
            current_stage=self._calculate_voice_stage(ai_age_days),
            age_days=ai_age_days
        )
        self.tts_profiles: Dict[str, TTSProfile] = {}
        self.sync_events: List[GuiVoiceSyncEvent] = []
        
        # Persona voice customization
        self.persona_voice: Optional[PersonaVoiceProfile] = None
        
        # Voice characteristics by stage
        self.stage_profiles = self._create_stage_profiles()
        
        # Current emotional modulation
        self.emotional_pitch_offset = 0.0
        self.emotional_speed_offset = 0.0
        self.current_emotion = EmotionalState.CALM
        
        # Voice blend state (for smooth transitions between stages)
        self.blend_progress = 0.0  # 0.0 to 1.0 for transitioning stages
        self.is_transitioning = False
        self.transition_start_time = None
        
        # TTS engine settings
        self.tts_engine = "device"  # "device", "google", "amazon", "azure"
        self.max_pitch = 2.0
        self.min_pitch = 0.5
        self.max_speed = 2.0
        self.min_speed = 0.5
    
    def _create_stage_profiles(self) -> Dict[VoiceStage, Dict]:
        """Create voice characteristics for each development stage."""
        return {
            VoiceStage.BABY: {
                "pitch_range": (1.5, 2.0),      # Higher pitched
                "speed_range": (0.7, 0.9),      # Slower speech
                "tone": VoiceTone.SOFT,
                "clarity": 0.7,
                "emotion_sensitivity": 0.3     # Emotions have less effect
            },
            VoiceStage.CHILD: {
                "pitch_range": (1.3, 1.7),
                "speed_range": (0.8, 1.0),
                "tone": VoiceTone.LIVELY,
                "clarity": 0.8,
                "emotion_sensitivity": 0.5
            },
            VoiceStage.TEENAGE: {
                "pitch_range": (1.0, 1.3),      # Voice cracking effect possible
                "speed_range": (0.9, 1.1),
                "tone": VoiceTone.ENERGETIC,
                "clarity": 0.85,
                "emotion_sensitivity": 0.7
            },
            VoiceStage.YOUNG_ADULT: {
                "pitch_range": (0.8, 1.1),
                "speed_range": (0.9, 1.1),
                "tone": VoiceTone.WARM,
                "clarity": 0.95,
                "emotion_sensitivity": 0.8
            },
            VoiceStage.MATURE: {
                "pitch_range": (0.7, 1.0),      # Lower, stable pitch
                "speed_range": (0.9, 1.1),
                "tone": VoiceTone.CALM,
                "clarity": 1.0,
                "emotion_sensitivity": 0.9     # Emotions integrated naturally
            }
        }
    
    def _calculate_voice_stage(self, age_days: int) -> VoiceStage:
        """Calculate voice stage based on AI age."""
        if age_days < 60:
            return VoiceStage.BABY
        elif age_days < 180:
            return VoiceStage.CHILD
        elif age_days < 365:
            return VoiceStage.TEENAGE
        elif age_days < 730:
            return VoiceStage.YOUNG_ADULT
        else:
            return VoiceStage.MATURE
    
    def update_age(self, new_age_days: int) -> None:
        """
        Update AI age and check for voice stage progression.
        
        Args:
            new_age_days: New age in days
        """
        self.ai_age_days = new_age_days
        new_stage = self._calculate_voice_stage(new_age_days)
        
        if new_stage != self.current_voice_state.current_stage:
            self._transition_to_stage(new_stage)
        
        self.current_voice_state.age_days = new_age_days
    
    def _transition_to_stage(self, new_stage: VoiceStage) -> None:
        """
        Smoothly transition voice to a new stage.
        
        Args:
            new_stage: Target voice stage
        """
        self.is_transitioning = True
        self.transition_start_time = datetime.now()
        self.blend_progress = 0.0
        
        # Transition takes 5 minutes (smooth blend)
        self.transition_duration = timedelta(minutes=5)
    
    def update_voice_transition(self) -> None:
        """Update voice blend during stage transition."""
        if not self.is_transitioning or not self.transition_start_time:
            return
        
        elapsed = datetime.now() - self.transition_start_time
        self.blend_progress = min(1.0, elapsed.total_seconds() / self.transition_duration.total_seconds())
        
        if self.blend_progress >= 1.0:
            self.is_transitioning = False
            self.blend_progress = 1.0
    
    def set_voice_preferences(self, preferences: VoicePreferences) -> None:
        """
        Update user's voice preferences.
        
        Args:
            preferences: VoicePreferences object
        """
        self.voice_preferences = preferences
        self.voice_preferences.last_updated = datetime.now()
        
        # Apply preferences to current voice state
        self.current_voice_state.gender = preferences.gender
        self.current_voice_state.current_tone = preferences.base_tone
        self.current_voice_state.current_pitch += preferences.pitch_offset
        self.current_voice_state.current_speed += preferences.speed_offset
        self.current_voice_state.volume_level = preferences.volume_level
    
    def update_emotion(self, emotion: EmotionalState) -> None:
        """
        Update voice modulation based on emotional state.
        
        Args:
            emotion: Current emotional state
        """
        self.current_emotion = emotion
        
        # Get current stage profile
        stage_profile = self.stage_profiles[self.current_voice_state.current_stage]
        emotion_sensitivity = stage_profile["emotion_sensitivity"]
        
        if not self.voice_preferences.enable_emotion_modulation:
            return
        
        # Map emotions to voice modulations
        emotion_modulations = {
            EmotionalState.HAPPY: {"pitch": 0.15, "speed": 0.1},
            EmotionalState.EXCITED: {"pitch": 0.25, "speed": 0.2},
            EmotionalState.CALM: {"pitch": -0.1, "speed": -0.1},
            EmotionalState.CONCERNED: {"pitch": -0.15, "speed": 0.05},
            EmotionalState.CURIOUS: {"pitch": 0.1, "speed": 0.05},
            EmotionalState.FOCUSED: {"pitch": 0.0, "speed": -0.05},
            EmotionalState.PLAYFUL: {"pitch": 0.2, "speed": 0.15},
            EmotionalState.PROTECTIVE: {"pitch": -0.1, "speed": 0.0}
        }
        
        modulation = emotion_modulations.get(emotion, {"pitch": 0.0, "speed": 0.0})
        
        # Apply emotional modulation with sensitivity scaling
        self.emotional_pitch_offset = modulation["pitch"] * emotion_sensitivity
        self.emotional_speed_offset = modulation["speed"] * emotion_sensitivity
        
        # Update current voice state
        self.current_voice_state.emotional_pitch_shift = self.emotional_pitch_offset
        self.current_voice_state.emotional_speed_shift = self.emotional_speed_offset
    
    def get_voice_parameters(self) -> Dict[str, float]:
        """
        Calculate final voice parameters considering all factors.
        
        Returns:
            Dictionary with pitch, speed, and tone parameters
        """
        stage_profile = self.stage_profiles[self.current_voice_state.current_stage]
        pitch_range = stage_profile["pitch_range"]
        speed_range = stage_profile["speed_range"]
        
        # Start with stage defaults
        pitch = (pitch_range[0] + pitch_range[1]) / 2
        speed = (speed_range[0] + speed_range[1]) / 2
        
        # Apply user preferences
        pitch += self.voice_preferences.pitch_offset
        speed += self.voice_preferences.speed_offset
        
        # Apply emotional modulation
        pitch += self.emotional_pitch_offset
        speed += self.emotional_speed_offset
        
        # Clamp to valid ranges
        pitch = max(self.min_pitch, min(self.max_pitch, pitch))
        speed = max(self.min_speed, min(self.max_speed, speed))
        
        # Apply voice blending if transitioning
        if self.is_transitioning and self.blend_progress < 1.0:
            # Blend between current and next stage
            current_pitch = pitch
            # Next stage would be calculated here
            # pitch = current_pitch * (1 - self.blend_progress) + next_stage_pitch * self.blend_progress
        
        return {
            "pitch": pitch,
            "speed": speed,
            "volume": self.voice_preferences.volume_level,
            "tone": stage_profile["tone"].value,
            "clarity": stage_profile["clarity"]
        }
    
    def synthesize_speech(self, text: str, facial_expression: FacialExpression) -> GuiVoiceSyncEvent:
        """
        Prepare speech synthesis with synchronized facial expression.
        
        Args:
            text: Text to synthesize
            facial_expression: Synchronized facial expression
        
        Returns:
            GuiVoiceSyncEvent for GUI synchronization
        """
        voice_params = self.get_voice_parameters()
        
        # Estimate duration (rough calculation: ~150 words per minute)
        word_count = len(text.split())
        duration_ms = int((word_count / 150) * 60 * 1000 / voice_params["speed"])
        
        sync_event = GuiVoiceSyncEvent(
            event_id=f"tts_{datetime.now().timestamp()}",
            event_type="speech_sync",
            facial_expression=facial_expression,
            voice_pitch=voice_params["pitch"],
            voice_speed=voice_params["speed"],
            duration_ms=duration_ms,
            text_to_speak=text,
            timestamp=datetime.now()
        )
        
        self.sync_events.append(sync_event)
        self.current_voice_state.is_speaking = True
        self.current_voice_state.current_text = text
        
        return sync_event
    
    def stop_speech(self) -> None:
        """Stop current speech."""
        self.current_voice_state.is_speaking = False
        self.current_voice_state.current_text = ""
    
    def get_voice_description(self) -> str:
        """Get human-readable description of current voice."""
        stage = self.current_voice_state.current_stage.value
        gender = self.voice_preferences.gender.value
        tone = self.voice_preferences.base_tone.value
        
        descriptions = {
            ("baby", "masculine", "soft"): "A sweet, high-pitched baby boy voice",
            ("baby", "feminine", "soft"): "A sweet, high-pitched baby girl voice",
            ("child", "masculine", "lively"): "A playful, young boy's voice",
            ("child", "feminine", "lively"): "A playful, young girl's voice",
            ("teenage", "masculine", "energetic"): "A growing teenage boy's voice",
            ("teenage", "feminine", "energetic"): "A growing teenage girl's voice",
            ("young_adult", "masculine", "warm"): "A warm, confident young man's voice",
            ("young_adult", "feminine", "warm"): "A warm, confident young woman's voice",
            ("mature", "masculine", "calm"): "A calm, mature man's voice",
            ("mature", "feminine", "calm"): "A calm, mature woman's voice",
        }
        
        return descriptions.get(
            (stage, gender, tone),
            f"An evolving {stage} {gender} voice with {tone} tone"
        )
    
    def get_voice_state(self) -> Dict[str, any]:
        """Get current voice state as dictionary."""
        return {
            "stage": self.current_voice_state.current_stage.value,
            "age_days": self.current_voice_state.age_days,
            "gender": self.voice_preferences.gender.value,
            "tone": self.voice_preferences.base_tone.value,
            "pitch": self.current_voice_state.current_pitch,
            "speed": self.current_voice_state.current_speed,
            "volume": self.voice_preferences.volume_level,
            "is_speaking": self.current_voice_state.is_speaking,
            "current_text": self.current_voice_state.current_text,
            "is_transitioning": self.is_transitioning,
            "transition_progress": self.blend_progress,
            "current_emotion": self.current_emotion.value,
            "description": self.get_voice_description(),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_voice_evolution_status(self) -> Dict[str, any]:
        """Get complete voice evolution status."""
        return {
            "ai_age_days": self.ai_age_days,
            "current_stage": self.current_voice_state.current_stage.value,
            "voice_state": self.get_voice_state(),
            "voice_parameters": self.get_voice_parameters(),
            "user_preferences": {
                "gender": self.voice_preferences.gender.value,
                "base_tone": self.voice_preferences.base_tone.value,
                "pitch_offset": self.voice_preferences.pitch_offset,
                "speed_offset": self.voice_preferences.speed_offset,
                "volume": self.voice_preferences.volume_level,
                "emotion_modulation": self.voice_preferences.enable_emotion_modulation,
                "auto_evolution": self.voice_preferences.auto_voice_evolution
            },
            "emotion_modulation": {
                "pitch_shift": self.emotional_pitch_offset,
                "speed_shift": self.emotional_speed_offset,
                "current_emotion": self.current_emotion.value
            },
            "sync_events_queued": len(self.sync_events),
            "last_updated": datetime.now().isoformat()
        }
    
    def set_persona_voice(self, persona_voice: PersonaVoiceProfile) -> bool:
        """Apply persona voice customization to voice engine"""
        self.persona_voice = persona_voice
        return True
    
    def get_voice_parameters_with_persona(self) -> Dict[str, float]:
        """Get voice parameters blended with persona voice style"""
        base_params = self.get_voice_parameters()
        
        if not self.persona_voice:
            return base_params
        
        adjusted = base_params.copy()
        adjusted["pitch"] = max(
            self.min_pitch, min(self.max_pitch,
                adjusted["pitch"] * self.persona_voice.pitch_offset
            )
        )
        adjusted["speed"] = max(
            self.min_speed, min(self.max_speed,
                adjusted["speed"] * self.persona_voice.speech_pace
            )
        )
        adjusted["volume"] = max(0.0, min(1.0,
            adjusted["volume"] * self.persona_voice.energy_level
        ))
        
        return adjusted
