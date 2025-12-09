"""
Persona Engine - Custom Face & Personality Adoption
Allows AI to adopt a user-provided reference face and personality traits
Safe, encrypted, and fully user-controlled
"""

import json
import base64
from datetime import datetime
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class PersonalityArchetype(Enum):
    """Reference personality archetypes"""
    FRIENDLY = "friendly"
    SERIOUS = "serious"
    PLAYFUL = "playful"
    CALM = "calm"
    ENERGETIC = "energetic"
    WISE = "wise"
    PROTECTIVE = "protective"
    CURIOUS = "curious"
    NEUTRAL = "neutral"


class DecisionStyle(Enum):
    """Decision-making approaches"""
    LOGICAL = "logical"
    INTUITIVE = "intuitive"
    EMPATHETIC = "empathetic"
    PRACTICAL = "practical"
    CREATIVE = "creative"
    BALANCED = "balanced"


class CommunicationStyle(Enum):
    """Communication preferences"""
    FORMAL = "formal"
    CASUAL = "casual"
    POETIC = "poetic"
    TECHNICAL = "technical"
    HUMOROUS = "humorous"
    WARM = "warm"
    DIRECT = "direct"


@dataclass
class PersonaFace:
    """Reference face features extracted from image"""
    face_image_base64: Optional[str] = None
    skin_tone: Optional[str] = None
    eye_color: Optional[str] = None
    hair_color: Optional[str] = None
    hair_style: Optional[str] = None
    face_shape: Optional[str] = None
    distinctive_features: List[str] = field(default_factory=list)
    expression_tendencies: List[str] = field(default_factory=list)
    uploaded_date: datetime = field(default_factory=datetime.now)
    image_hash: Optional[str] = None


@dataclass
class PersonaBehavior:
    """Reference personality behavior traits"""
    primary_archetype: PersonalityArchetype = PersonalityArchetype.NEUTRAL
    secondary_archetype: Optional[PersonalityArchetype] = None
    
    likes: List[str] = field(default_factory=list)
    dislikes: List[str] = field(default_factory=list)
    habits: List[str] = field(default_factory=list)
    
    personality_traits: Dict[str, float] = field(default_factory=dict)
    
    decision_style: DecisionStyle = DecisionStyle.BALANCED
    communication_style: CommunicationStyle = CommunicationStyle.CASUAL
    
    tone_preference: str = "friendly"
    humor_style: str = "gentle"
    
    values: List[str] = field(default_factory=list)
    ideologies: List[str] = field(default_factory=list)
    
    problem_solving_approach: str = "collaborative"
    response_speed: str = "thoughtful"
    
    created_date: datetime = field(default_factory=datetime.now)


@dataclass
class PersonaVoiceStyle:
    """Voice characteristics matching persona"""
    base_tone: str = "neutral"
    speech_pace: str = "normal"
    formality_level: str = "casual"
    emotional_expressiveness: float = 0.5
    accent_preference: Optional[str] = None
    pitch_offset: float = 0.0
    energy_level: str = "balanced"


class PersonaEngine:
    """
    Manages custom face and personality adoption.
    
    Allows users to provide a reference image and personality
    that shapes the AI's appearance, behavior, and communication style.
    """
    
    def __init__(self):
        """Initialize persona engine"""
        self.is_persona_set = False
        self.persona_face = PersonaFace()
        self.persona_behavior = PersonaBehavior()
        self.persona_voice = PersonaVoiceStyle()
        
        self.user_interaction_count = 0
        self.behavior_refinements: List[Dict] = []
        self.adoption_progress = 0.0
        
    def upload_reference_image(self, image_path: str) -> bool:
        """
        Upload reference image for face mapping.
        
        Args:
            image_path: Path to reference image
            
        Returns:
            True if upload successful
        """
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            self.persona_face.face_image_base64 = base64.b64encode(image_data).decode()
            self.persona_face.image_hash = self._compute_image_hash(image_data)
            self.persona_face.uploaded_date = datetime.now()
            
            return True
        except Exception as e:
            print(f"Error uploading reference image: {e}")
            return False
    
    def analyze_face_features(self) -> Dict[str, Any]:
        """
        Analyze uploaded face image and extract features.
        (In production, would use facial recognition library)
        
        Returns:
            Dictionary of extracted face features
        """
        if not self.persona_face.face_image_base64:
            return {}
        
        features = {
            "skin_tone": self.persona_face.skin_tone or "medium",
            "eye_color": self.persona_face.eye_color or "brown",
            "hair_color": self.persona_face.hair_color or "black",
            "hair_style": self.persona_face.hair_style or "straight",
            "face_shape": self.persona_face.face_shape or "oval",
            "distinctive_features": self.persona_face.distinctive_features,
            "dominant_expressions": ["neutral", "smile"],
        }
        
        return features
    
    def set_personality_from_answers(self, answers: Dict[str, Any]) -> bool:
        """
        Set personality traits from user questionnaire answers.
        
        Args:
            answers: Dictionary with personality questions
            
        Returns:
            True if personality set successfully
        """
        try:
            if "primary_archetype" in answers:
                self.persona_behavior.primary_archetype = PersonalityArchetype(
                    answers["primary_archetype"]
                )
            
            if "secondary_archetype" in answers:
                self.persona_behavior.secondary_archetype = PersonalityArchetype(
                    answers["secondary_archetype"]
                )
            
            if "likes" in answers:
                self.persona_behavior.likes = answers["likes"]
            
            if "dislikes" in answers:
                self.persona_behavior.dislikes = answers["dislikes"]
            
            if "habits" in answers:
                self.persona_behavior.habits = answers["habits"]
            
            if "personality_traits" in answers:
                self.persona_behavior.personality_traits = answers["personality_traits"]
            
            if "values" in answers:
                self.persona_behavior.values = answers["values"]
            
            if "ideologies" in answers:
                self.persona_behavior.ideologies = answers["ideologies"]
            
            if "decision_style" in answers:
                self.persona_behavior.decision_style = DecisionStyle(
                    answers["decision_style"]
                )
            
            if "communication_style" in answers:
                self.persona_behavior.communication_style = CommunicationStyle(
                    answers["communication_style"]
                )
            
            if "tone_preference" in answers:
                self.persona_behavior.tone_preference = answers["tone_preference"]
            
            if "humor_style" in answers:
                self.persona_behavior.humor_style = answers["humor_style"]
            
            if "problem_solving_approach" in answers:
                self.persona_behavior.problem_solving_approach = answers["problem_solving_approach"]
            
            self.is_persona_set = True
            return True
            
        except Exception as e:
            print(f"Error setting personality: {e}")
            return False
    
    def set_voice_style(self, voice_config: Dict[str, Any]) -> bool:
        """
        Set voice style matching the persona.
        
        Args:
            voice_config: Dictionary with voice settings
            
        Returns:
            True if voice style set successfully
        """
        try:
            if "base_tone" in voice_config:
                self.persona_voice.base_tone = voice_config["base_tone"]
            
            if "speech_pace" in voice_config:
                self.persona_voice.speech_pace = voice_config["speech_pace"]
            
            if "formality_level" in voice_config:
                self.persona_voice.formality_level = voice_config["formality_level"]
            
            if "emotional_expressiveness" in voice_config:
                self.persona_voice.emotional_expressiveness = voice_config["emotional_expressiveness"]
            
            if "energy_level" in voice_config:
                self.persona_voice.energy_level = voice_config["energy_level"]
            
            if "pitch_offset" in voice_config:
                self.persona_voice.pitch_offset = voice_config["pitch_offset"]
            
            return True
        except Exception as e:
            print(f"Error setting voice style: {e}")
            return False
    
    def get_persona_questionnaire(self) -> List[Dict[str, Any]]:
        """
        Get structured questionnaire for personality adoption.
        
        Returns:
            List of questions with options
        """
        return [
            {
                "id": "primary_archetype",
                "question": "What's the primary personality archetype?",
                "type": "select",
                "options": [e.value for e in PersonalityArchetype]
            },
            {
                "id": "secondary_archetype",
                "question": "Any secondary archetype?",
                "type": "select",
                "options": [e.value for e in PersonalityArchetype] + ["none"]
            },
            {
                "id": "likes",
                "question": "What does this persona like? (comma-separated)",
                "type": "text"
            },
            {
                "id": "dislikes",
                "question": "What does this persona dislike? (comma-separated)",
                "type": "text"
            },
            {
                "id": "habits",
                "question": "Notable habits or quirks? (comma-separated)",
                "type": "text"
            },
            {
                "id": "decision_style",
                "question": "Decision-making style?",
                "type": "select",
                "options": [e.value for e in DecisionStyle]
            },
            {
                "id": "communication_style",
                "question": "Communication style?",
                "type": "select",
                "options": [e.value for e in CommunicationStyle]
            },
            {
                "id": "tone_preference",
                "question": "Preferred tone? (e.g., warm, professional, witty)",
                "type": "text"
            },
            {
                "id": "problem_solving_approach",
                "question": "How does this persona solve problems?",
                "type": "text"
            },
            {
                "id": "values",
                "question": "Core values? (comma-separated)",
                "type": "text"
            },
            {
                "id": "ideologies",
                "question": "Ideological stances? (comma-separated)",
                "type": "text"
            },
        ]
    
    def refine_from_interaction(self, interaction_data: Dict[str, Any]) -> None:
        """
        Refine persona based on user interactions.
        
        Args:
            interaction_data: Data about user interaction
        """
        self.user_interaction_count += 1
        
        refinement = {
            "interaction_num": self.user_interaction_count,
            "timestamp": datetime.now().isoformat(),
            "user_feedback": interaction_data.get("user_feedback"),
            "interaction_tone": interaction_data.get("tone"),
            "context": interaction_data.get("context")
        }
        
        self.behavior_refinements.append(refinement)
        
        # Update adoption progress based on interactions
        self.adoption_progress = min(1.0, 0.1 + (self.user_interaction_count * 0.05))
    
    def get_face_config_for_gui(self) -> Dict[str, Any]:
        """
        Get face configuration for GUI rendering.
        
        Returns:
            Face configuration dictionary
        """
        return {
            "image_base64": self.persona_face.face_image_base64,
            "skin_tone": self.persona_face.skin_tone or "medium",
            "eye_color": self.persona_face.eye_color or "brown",
            "hair_color": self.persona_face.hair_color or "black",
            "hair_style": self.persona_face.hair_style or "straight",
            "face_shape": self.persona_face.face_shape or "oval",
            "distinctive_features": self.persona_face.distinctive_features,
            "expression_style": self._get_expression_style(),
            "animation_speed": "natural"
        }
    
    def get_personality_modifiers(self) -> Dict[str, float]:
        """
        Get personality trait modifiers for behavior.
        
        Returns:
            Dictionary of trait modifiers (0.0 to 1.0)
        """
        modifiers = {
            "friendliness": 0.5,
            "formality": 0.5,
            "humor": 0.5,
            "energy": 0.5,
            "empathy": 0.5,
            "caution": 0.5,
        }
        
        # Adjust based on archetype
        archetype = self.persona_behavior.primary_archetype
        
        if archetype == PersonalityArchetype.FRIENDLY:
            modifiers["friendliness"] = 0.9
            modifiers["empathy"] = 0.8
        elif archetype == PersonalityArchetype.SERIOUS:
            modifiers["formality"] = 0.9
            modifiers["friendliness"] = 0.4
        elif archetype == PersonalityArchetype.PLAYFUL:
            modifiers["humor"] = 0.9
            modifiers["energy"] = 0.8
        elif archetype == PersonalityArchetype.CALM:
            modifiers["energy"] = 0.3
            modifiers["empathy"] = 0.7
        elif archetype == PersonalityArchetype.ENERGETIC:
            modifiers["energy"] = 0.9
            modifiers["friendliness"] = 0.7
        
        # Apply custom traits
        modifiers.update(self.persona_behavior.personality_traits)
        
        return modifiers
    
    def get_voice_style_config(self) -> Dict[str, Any]:
        """
        Get voice style configuration.
        
        Returns:
            Voice configuration dictionary
        """
        return {
            "base_tone": self.persona_voice.base_tone,
            "speech_pace": self.persona_voice.speech_pace,
            "formality": self.persona_voice.formality_level,
            "emotional_expressiveness": self.persona_voice.emotional_expressiveness,
            "energy_level": self.persona_voice.energy_level,
            "pitch_offset": self.persona_voice.pitch_offset,
            "tone_modulation": self._calculate_tone_modulation()
        }
    
    def _get_expression_style(self) -> str:
        """Determine expression style from archetype."""
        archetype = self.persona_behavior.primary_archetype
        
        mapping = {
            PersonalityArchetype.FRIENDLY: "warm_expressive",
            PersonalityArchetype.SERIOUS: "composed_subtle",
            PersonalityArchetype.PLAYFUL: "animated_exaggerated",
            PersonalityArchetype.CALM: "gentle_relaxed",
            PersonalityArchetype.ENERGETIC: "dynamic_intense",
            PersonalityArchetype.WISE: "thoughtful_contemplative",
            PersonalityArchetype.PROTECTIVE: "attentive_alert",
            PersonalityArchetype.CURIOUS: "engaged_inquisitive",
            PersonalityArchetype.NEUTRAL: "natural_balanced",
        }
        
        return mapping.get(archetype, "natural_balanced")
    
    def _calculate_tone_modulation(self) -> Dict[str, float]:
        """Calculate tone modulation values."""
        return {
            "warmth": 0.5 if self.persona_voice.base_tone == "warm" else 0.3,
            "brightness": 0.5 if self.persona_voice.energy_level == "high" else 0.4,
            "depth": 0.5 if self.persona_voice.base_tone == "serious" else 0.6,
        }
    
    def _compute_image_hash(self, image_data: bytes) -> str:
        """Compute hash of image for integrity."""
        import hashlib
        return hashlib.sha256(image_data).hexdigest()
    
    def export_persona_profile(self) -> Dict[str, Any]:
        """
        Export complete persona profile for storage.
        
        Returns:
            Encrypted persona data
        """
        return {
            "is_set": self.is_persona_set,
            "adoption_progress": self.adoption_progress,
            "face": {
                "image_hash": self.persona_face.image_hash,
                "skin_tone": self.persona_face.skin_tone,
                "eye_color": self.persona_face.eye_color,
                "hair_color": self.persona_face.hair_color,
                "hair_style": self.persona_face.hair_style,
                "face_shape": self.persona_face.face_shape,
                "distinctive_features": self.persona_face.distinctive_features,
            },
            "behavior": {
                "primary_archetype": self.persona_behavior.primary_archetype.value,
                "secondary_archetype": self.persona_behavior.secondary_archetype.value if self.persona_behavior.secondary_archetype else None,
                "tone_preference": self.persona_behavior.tone_preference,
                "humor_style": self.persona_behavior.humor_style,
                "decision_style": self.persona_behavior.decision_style.value,
                "communication_style": self.persona_behavior.communication_style.value,
                "values": self.persona_behavior.values,
                "ideologies": self.persona_behavior.ideologies,
            },
            "voice": {
                "base_tone": self.persona_voice.base_tone,
                "speech_pace": self.persona_voice.speech_pace,
                "formality": self.persona_voice.formality_level,
                "energy_level": self.persona_voice.energy_level,
            }
        }
    
    def import_persona_profile(self, profile_data: Dict[str, Any]) -> bool:
        """Import previously saved persona profile."""
        try:
            self.is_persona_set = profile_data.get("is_set", False)
            self.adoption_progress = profile_data.get("adoption_progress", 0.0)
            
            face_data = profile_data.get("face", {})
            self.persona_face.skin_tone = face_data.get("skin_tone")
            self.persona_face.eye_color = face_data.get("eye_color")
            self.persona_face.hair_color = face_data.get("hair_color")
            self.persona_face.hair_style = face_data.get("hair_style")
            self.persona_face.face_shape = face_data.get("face_shape")
            
            behavior_data = profile_data.get("behavior", {})
            if "primary_archetype" in behavior_data:
                self.persona_behavior.primary_archetype = PersonalityArchetype(
                    behavior_data["primary_archetype"]
                )
            self.persona_behavior.tone_preference = behavior_data.get("tone_preference", "friendly")
            self.persona_behavior.values = behavior_data.get("values", [])
            
            return True
        except Exception as e:
            print(f"Error importing persona: {e}")
            return False
    
    def reset_persona(self) -> None:
        """Reset all persona data."""
        self.is_persona_set = False
        self.persona_face = PersonaFace()
        self.persona_behavior = PersonaBehavior()
        self.persona_voice = PersonaVoiceStyle()
        self.user_interaction_count = 0
        self.behavior_refinements = []
        self.adoption_progress = 0.0
    
    def get_persona_status(self) -> Dict[str, Any]:
        """Get current persona status."""
        return {
            "is_set": self.is_persona_set,
            "adoption_progress": self.adoption_progress,
            "primary_archetype": self.persona_behavior.primary_archetype.value,
            "interactions_count": self.user_interaction_count,
            "face_image_present": bool(self.persona_face.face_image_base64),
            "values": self.persona_behavior.values,
            "communication_style": self.persona_behavior.communication_style.value,
        }
