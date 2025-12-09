"""
Project Mind - GUI Face Engine
Manages the animated face/avatar that expresses the AI's emotions and interactions.

This engine creates a living, expressive face that:
- Displays emotions through facial expressions
- Animates naturally (blinking, nodding, gestures)
- Syncs with voice and dialogue
- Adapts appearance based on user preferences
- Optimizes rendering for device capabilities
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum

from src.types import (
    FaceStyle, SkinTone, FacialExpression, ExpressionIntensity,
    FacePreferences, FacialState, GUIAsset, EmotionalState, PersonaFaceProfile
)


class GuiEngine:
    """
    Manages the animated face/GUI presentation of the AI.
    
    Features:
    - Real-time facial expression rendering
    - Natural blinking and micro-expressions
    - Emotion-driven expressions
    - Customizable appearance
    - Lightweight rendering optimized for phone specs
    """
    
    def __init__(self, device_capability: str = "mid_range"):
        """
        Initialize the GUI Engine.
        
        Args:
            device_capability: "low_end", "mid_range", or "high_end" for rendering quality
        """
        self.device_capability = device_capability
        self.face_preferences = FacePreferences()
        self.current_facial_state = FacialState()
        self.gui_assets: Dict[str, GUIAsset] = {}
        self.is_visible = False
        self.render_mode = "widget"  # "widget", "overlay", "fullscreen"
        self.animation_queue: List[FacialExpression] = []
        self.blink_timer = 0.0
        
        # Persona face profile (optional custom reference)
        self.persona_face: Optional[PersonaFaceProfile] = None
        self.last_blink = datetime.now()
        self.default_blink_interval = 3.0  # seconds
        self.micro_expression_history: List[Tuple[FacialExpression, datetime]] = []
        
        # Optimization settings
        self.fps_target = 30 if device_capability == "low_end" else 60
        self.animation_quality = {
            "low_end": "simple",      # Basic shapes and colors
            "mid_range": "standard",  # Smooth animations
            "high_end": "detailed"    # High-detail with shaders
        }[device_capability]
        
        # Asset management
        self._load_face_assets()
    
    def _load_face_assets(self) -> None:
        """Load or cache face assets for quick rendering."""
        base_assets = [
            "face_base", "eyes_open", "eyes_closed", "mouth_smile",
            "mouth_neutral", "eyebrows_neutral", "eyebrows_raised",
            "eyebrows_furrowed", "nose", "ears"
        ]
        
        for asset_name in base_assets:
            self.gui_assets[asset_name] = GUIAsset(
                asset_id=asset_name,
                asset_type=asset_name.split("_")[0],
                file_path=f"assets/faces/{asset_name}.svg",
                format="svg",
                size_kb=5.0,
                cached=True
            )
    
    def set_face_preferences(self, preferences: FacePreferences) -> None:
        """
        Update face appearance preferences.
        
        Args:
            preferences: FacePreferences object with style, skin tone, etc.
        """
        self.face_preferences = preferences
        self.face_preferences.last_updated = datetime.now()
        self._trigger_face_update()
    
    def update_facial_expression(self, 
                                 emotion: EmotionalState,
                                 intensity: ExpressionIntensity = ExpressionIntensity.MODERATE) -> None:
        """
        Update facial expression based on emotional state.
        
        Args:
            emotion: Current emotional state
            intensity: How intense the expression should be
        """
        # Map emotional states to facial expressions
        emotion_to_expression = {
            EmotionalState.HAPPY: FacialExpression.HAPPY,
            EmotionalState.CURIOUS: FacialExpression.CURIOUS,
            EmotionalState.CONCERNED: FacialExpression.CONCERNED,
            EmotionalState.EXCITED: FacialExpression.EXCITED,
            EmotionalState.CALM: FacialExpression.CALM,
            EmotionalState.FOCUSED: FacialExpression.THINKING,
            EmotionalState.PLAYFUL: FacialExpression.SMILE,
            EmotionalState.PROTECTIVE: FacialExpression.CONCERNED
        }
        
        expression = emotion_to_expression.get(emotion, FacialExpression.NEUTRAL)
        self.animate_expression(expression, intensity)
    
    def animate_expression(self, 
                          expression: FacialExpression,
                          intensity: ExpressionIntensity = ExpressionIntensity.MODERATE,
                          duration_ms: int = 500) -> None:
        """
        Animate a facial expression with smooth transitions.
        
        Args:
            expression: Target facial expression
            intensity: Intensity of the expression
            duration_ms: Duration of animation in milliseconds
        """
        self.current_facial_state.expression = expression
        self.current_facial_state.intensity = intensity
        self.current_facial_state.timestamp = datetime.now()
        
        # Set expression-specific parameters
        if expression == FacialExpression.HAPPY:
            self.current_facial_state.mouth_opening = 0.6 if intensity == ExpressionIntensity.ANIMATED else 0.4
            self.current_facial_state.eyebrow_position = 0.7
        elif expression == FacialExpression.CURIOUS:
            self.current_facial_state.eyebrow_position = 0.8
            self.current_facial_state.mouth_opening = 0.1
            self.current_facial_state.eye_position = (0.5, 0.4)  # Eyes widened
        elif expression == FacialExpression.CONCERNED:
            self.current_facial_state.eyebrow_position = 0.2
            self.current_facial_state.mouth_opening = 0.2
            self.current_facial_state.eye_position = (0.5, 0.5)
        elif expression == FacialExpression.EXCITED:
            self.current_facial_state.mouth_opening = 0.8
            self.current_facial_state.eyebrow_position = 0.8
            self.current_facial_state.eye_position = (0.5, 0.3)  # Eyes wide
        elif expression == FacialExpression.THINKING:
            self.current_facial_state.mouth_opening = 0.15
            self.current_facial_state.eyebrow_position = 0.5
            self.current_facial_state.eye_position = (0.6, 0.5)  # Eyes looking up-right
        elif expression == FacialExpression.LISTENING:
            self.current_facial_state.mouth_opening = 0.0
            self.current_facial_state.eyebrow_position = 0.6
        elif expression == FacialExpression.SPEAKING:
            self.current_facial_state.is_speaking = True
            self.current_facial_state.mouth_opening = 0.5  # Animates with audio
        
        self.animation_queue.append(expression)
        self._log_micro_expression(expression)
    
    def handle_blink(self, force: bool = False) -> None:
        """
        Trigger a natural blink animation.
        
        Args:
            force: Force blink regardless of timer
        """
        now = datetime.now()
        time_since_blink = (now - self.last_blink).total_seconds()
        
        if force or time_since_blink >= self.default_blink_interval:
            self.current_facial_state.is_blinking = True
            self.current_facial_state.animation_frame = 0
            self.last_blink = now
            self.animation_queue.append(FacialExpression.BLINKING)
            self._log_micro_expression(FacialExpression.BLINKING)
    
    def handle_nod(self, direction: str = "vertical", intensity: float = 0.5) -> None:
        """
        Trigger a nod or head gesture.
        
        Args:
            direction: "vertical" or "horizontal"
            intensity: Intensity of the gesture (0.0 to 1.0)
        """
        self.animation_queue.append(FacialExpression.NODDING)
        self.current_facial_state.animation_speed = 1.0 + intensity
        self._log_micro_expression(FacialExpression.NODDING)
    
    def sync_with_speech(self, text: str, duration_ms: int) -> None:
        """
        Sync facial animation with speech output.
        
        Args:
            text: Text being spoken
            duration_ms: Duration of speech in milliseconds
        """
        self.current_facial_state.is_speaking = True
        self.current_facial_state.current_text = text
        self.animate_expression(FacialExpression.SPEAKING)
        
        # Calculate mouth animation based on text length and duration
        self.current_facial_state.mouth_opening = min(0.8, len(text) / 100)
    
    def stop_speaking(self) -> None:
        """Stop speech animation and return to neutral."""
        self.current_facial_state.is_speaking = False
        self.current_facial_state.current_text = ""
        self.animate_expression(FacialExpression.NEUTRAL)
    
    def render_frame(self) -> Dict[str, any]:
        """
        Generate rendering data for current frame.
        
        Returns:
            Dictionary containing rendering instructions for the UI layer
        """
        frame_data = {
            "timestamp": datetime.now().isoformat(),
            "expression": self.current_facial_state.expression.value,
            "intensity": self.current_facial_state.intensity.value,
            "eye_position": self.current_facial_state.eye_position,
            "mouth_opening": self.current_facial_state.mouth_opening,
            "eyebrow_position": self.current_facial_state.eyebrow_position,
            "is_blinking": self.current_facial_state.is_blinking,
            "is_speaking": self.current_facial_state.is_speaking,
            "animation_speed": self.current_facial_state.animation_speed,
            "style": self.face_preferences.style.value,
            "skin_tone": self.face_preferences.skin_tone.value,
            "eye_color": self.face_preferences.eye_color,
            "quality": self.animation_quality,
            "fps": self.fps_target
        }
        return frame_data
    
    def get_facial_state(self) -> Dict[str, any]:
        """Get current facial state as dictionary."""
        return {
            "expression": self.current_facial_state.expression.value,
            "intensity": self.current_facial_state.intensity.value,
            "is_blinking": self.current_facial_state.is_blinking,
            "is_speaking": self.current_facial_state.is_speaking,
            "eye_position": self.current_facial_state.eye_position,
            "mouth_opening": self.current_facial_state.mouth_opening,
            "eyebrow_position": self.current_facial_state.eyebrow_position,
            "timestamp": self.current_facial_state.timestamp.isoformat()
        }
    
    def _trigger_face_update(self) -> None:
        """Trigger a full face appearance update."""
        # This would be called when preferences change to reload/regenerate face assets
        pass
    
    def _log_micro_expression(self, expression: FacialExpression) -> None:
        """Log micro-expressions for personality tracking."""
        self.micro_expression_history.append((expression, datetime.now()))
        # Keep only recent history (last 100 expressions)
        if len(self.micro_expression_history) > 100:
            self.micro_expression_history.pop(0)
    
    def get_micro_expression_summary(self) -> Dict[str, int]:
        """Get summary of recent micro-expressions."""
        summary = {}
        for expr, _ in self.micro_expression_history:
            summary[expr.value] = summary.get(expr.value, 0) + 1
        return summary
    
    def set_visibility(self, visible: bool, mode: str = "widget") -> None:
        """
        Control GUI visibility.
        
        Args:
            visible: Show or hide the face
            mode: "widget" (small), "overlay" (floating), "fullscreen"
        """
        self.is_visible = visible
        self.render_mode = mode
    
    def optimize_for_battery(self, battery_percent: int) -> None:
        """
        Reduce animation quality when battery is low.
        
        Args:
            battery_percent: Current battery percentage
        """
        if battery_percent < 20:
            self.fps_target = 15
            self.animation_quality = "simple"
        elif battery_percent < 50:
            self.fps_target = 30
            self.animation_quality = "simple" if self.device_capability == "low_end" else "standard"
    
    def set_persona_face(self, persona_face: PersonaFaceProfile) -> bool:
        """
        Set persona reference face for custom appearance.
        
        Args:
            persona_face: Persona face profile with features
            
        Returns:
            True if persona face set successfully
        """
        self.persona_face = persona_face
        
        # Apply persona face customizations
        if persona_face.skin_tone:
            self.face_preferences.skin_tone = SkinTone(persona_face.skin_tone)
        if persona_face.eye_color:
            self.face_preferences.eye_color = persona_face.eye_color
        if persona_face.hair_color:
            # Store as preference (would need to extend FacePreferences)
            pass
        
        return True
    
    def get_persona_face_render(self) -> Optional[Dict]:
        """
        Get render instructions for persona custom face.
        
        Returns:
            Persona face render specification
        """
        if not self.persona_face:
            return None
        
        return {
            "type": "persona_custom",
            "skin_tone": self.persona_face.skin_tone,
            "eye_color": self.persona_face.eye_color,
            "hair_color": self.persona_face.hair_color,
            "hair_style": self.persona_face.hair_style,
            "face_shape": self.persona_face.face_shape,
            "distinctive_features": self.persona_face.distinctive_features,
            "expression_style": self.persona_face.expression_style
        }
    
    def get_gui_status(self) -> Dict[str, any]:
        """Get complete GUI engine status."""
        status = {
            "visible": self.is_visible,
            "render_mode": self.render_mode,
            "device_capability": self.device_capability,
            "animation_quality": self.animation_quality,
            "fps_target": self.fps_target,
            "facial_state": self.get_facial_state(),
            "face_preferences": {
                "style": self.face_preferences.style.value,
                "skin_tone": self.face_preferences.skin_tone.value,
                "expression_intensity": self.face_preferences.expression_intensity.value,
                "eye_color": self.face_preferences.eye_color
            },
            "animation_queue_length": len(self.animation_queue),
            "micro_expressions_tracked": len(self.micro_expression_history),
            "has_persona_face": bool(self.persona_face),
            "last_updated": datetime.now().isoformat()
        }
        return status
