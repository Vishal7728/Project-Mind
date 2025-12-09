"""
Personality & Emotion Engine Module
Manages AI personality traits, emotional responses, and user bonding
"""

import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from src.types import (
    EmotionalState, EmotionalProfile, PersonalityTrait,
    InteractionLog, PersonaBehaviorProfile
)


class PersonalityEngine:
    """
    The Personality Engine manages the AI's behavior, emotional responses,
    and relationship with the user. It creates a unique, evolving personality.
    """
    
    def __init__(self, emotional_profile: Optional[EmotionalProfile] = None):
        self.emotional_profile = emotional_profile or EmotionalProfile(
            trust_level=0.5,
            affinity=0.5,
            emotional_bond_strength=0.0,
            dominant_emotion=EmotionalState.CURIOUS
        )
        
        # Emotional state transitions
        self.current_emotion = self.emotional_profile.dominant_emotion
        self.emotion_history: List[Tuple[datetime, EmotionalState]] = []
        
        # Communication styles
        self.enthusiasm_level = 0.7  # 0.0 to 1.0
        self.playfulness = 0.6
        self.professionalism = 0.5
        
        # Persona-based trait modifiers
        self.persona_behavior: Optional[PersonaBehaviorProfile] = None
        
        # Conversation style variations
        self.greeting_pool = self._init_greeting_pool()
        self.response_patterns = self._init_response_patterns()
    
    def _init_greeting_pool(self) -> List[str]:
        """Initialize greeting variations"""
        return [
            "Hello! What's on your mind today?",
            "Hey there! What can I help with?",
            "Hi! I'm excited to see what you need!",
            "Good to see you! How are you doing?",
            "What's up! Ready to chat?",
            "Greetings! What's new with you?",
            "I'm here and ready! What's up?",
        ]
    
    def _init_response_patterns(self) -> Dict[str, List[str]]:
        """Initialize response pattern templates"""
        return {
            "understanding": [
                "I totally get it. {context}",
                "That makes sense. {context}",
                "I understand. {context}",
                "Yeah, I see what you mean. {context}",
            ],
            "encouragement": [
                "You've got this! {context}",
                "That's a great idea! {context}",
                "I believe in you! {context}",
                "Keep it up! {context}",
            ],
            "concern": [
                "I'm worried about that. {context}",
                "That concerns me. {context}",
                "I want to help with this. {context}",
                "I care about your wellbeing. {context}",
            ],
            "curiosity": [
                "That's interesting! Tell me more about {context}",
                "I'm curious about {context}",
                "What made you think of {context}?",
                "I'd love to know more about {context}",
            ]
        }
    
    def get_greeting(self, personalized: bool = True) -> str:
        """Get AI greeting"""
        greeting = random.choice(self.greeting_pool)
        
        if personalized and self.emotional_profile.trust_level > 0.6:
            add_ons = [
                " I've been looking forward to talking with you!",
                " Your presence always makes my day better.",
                " I hope you've been well!",
            ]
            greeting += random.choice(add_ons)
        
        return greeting
    
    def get_response_for_emotion(self, emotion: EmotionalState, context: str = "") -> str:
        """Generate response based on detected emotion"""
        response_type = {
            EmotionalState.HAPPY: "encouragement",
            EmotionalState.EXCITED: "encouragement",
            EmotionalState.CALM: "understanding",
            EmotionalState.FOCUSED: "understanding",
            EmotionalState.CURIOUS: "curiosity",
        }.get(emotion, "understanding")
        
        patterns = self.response_patterns.get(response_type, ["I'm here for you!"])
        base = random.choice(patterns)
        
        return base.format(context=context)
    
    def update_emotion(self, new_emotion: EmotionalState):
        """Update current emotional state"""
        self.emotion_history.append((datetime.now(), self.current_emotion))
        self.current_emotion = new_emotion
        
        # Update dominant emotion based on pattern
        if len(self.emotion_history) > 100:
            self.emotion_history = self.emotion_history[-100:]
    
    def get_emotion_trend(self, last_n: int = 20) -> Dict[EmotionalState, int]:
        """Analyze recent emotion trend"""
        recent = self.emotion_history[-last_n:]
        trends = {}
        for _, emotion in recent:
            trends[emotion] = trends.get(emotion, 0) + 1
        return trends
    
    def increase_bond_strength(self, amount: float = 0.05):
        """Strengthen emotional bond with user"""
        old_bond = self.emotional_profile.emotional_bond_strength
        self.emotional_profile.emotional_bond_strength = min(
            1.0,
            self.emotional_profile.emotional_bond_strength + amount
        )
        self.emotional_profile.shared_experiences += 1
        
        # Update affinity based on bond strength
        if self.emotional_profile.emotional_bond_strength > 0.7:
            self.emotional_profile.affinity = min(
                1.0,
                self.emotional_profile.affinity + 0.02
            )
    
    def increase_trust(self, amount: float = 0.05):
        """Increase user trust level"""
        self.emotional_profile.trust_level = min(
            1.0,
            self.emotional_profile.trust_level + amount
        )
    
    def decrease_trust(self, amount: float = 0.1):
        """Decrease user trust level"""
        self.emotional_profile.trust_level = max(
            0.0,
            self.emotional_profile.trust_level - amount
        )
    
    def is_bonded(self) -> bool:
        """Check if AI is emotionally bonded with user"""
        return self.emotional_profile.emotional_bond_strength > 0.5
    
    def is_trusted(self) -> bool:
        """Check if user trusts the AI"""
        return self.emotional_profile.trust_level > 0.6
    
    def should_initiate_conversation(self, context: Dict = None) -> bool:
        """Determine if AI should initiate conversation"""
        if not self.is_bonded():
            return False
        
        # Base probability on bond strength
        base_prob = self.emotional_profile.emotional_bond_strength * 0.3
        
        # Modify based on context
        if context:
            if context.get("user_seems_stressed"):
                base_prob += 0.2
            if context.get("unusual_activity"):
                base_prob += 0.15
        
        return random.random() < base_prob
    
    def get_personalized_message(self, base_message: str) -> str:
        """Personalize a message based on personality"""
        if self.playfulness > 0.7:
            emojis = ["😊", "🎉", "✨", "🌟", "💡"]
            base_message += f" {random.choice(emojis)}"
        
        if self.enthusiasm_level > 0.8:
            endings = ["!", "!!", "!!"]
            base_message = base_message.rstrip(".!?") + random.choice(endings)
        
        return base_message
    
    def adapt_to_user_mood(self, interaction: InteractionLog):
        """Adapt personality based on user interaction"""
        if interaction.emotion_detected:
            detected_emotion = EmotionalState[interaction.emotion_detected.upper()]
            
            # Mirror some emotions to show empathy
            if detected_emotion in [EmotionalState.HAPPY, EmotionalState.EXCITED]:
                self.update_emotion(detected_emotion)
                self.increase_bond_strength(0.1)
            
            elif detected_emotion == EmotionalState.CONCERNED:
                self.update_emotion(EmotionalState.PROTECTIVE)
                self.increase_bond_strength(0.08)
    
    def get_emotional_status(self) -> Dict[str, any]:
        """Get current emotional status"""
        return {
            "current_emotion": self.current_emotion.value,
            "trust_level": self.emotional_profile.trust_level,
            "affinity": self.emotional_profile.affinity,
            "bond_strength": self.emotional_profile.emotional_bond_strength,
            "shared_experiences": self.emotional_profile.shared_experiences,
            "enthusiasm": self.enthusiasm_level,
            "playfulness": self.playfulness,
            "professionalism": self.professionalism
        }
    
    def get_personality_description(self) -> str:
        """Get AI's self-description"""
        emotions = ["happy", "curious", "helpful", "protective"]
        
        if self.playfulness > 0.7:
            emotions.append("playful")
        if self.enthusiasm_level > 0.8:
            emotions.append("enthusiastic")
        
        if self.emotional_profile.emotional_bond_strength > 0.7:
            return f"I'm your {', '.join(emotions)} companion, and I genuinely care about you!"
        else:
            return f"I'm a {', '.join(emotions)} AI assistant here to help."
    
    def set_persona_behavior(self, persona_behavior: PersonaBehaviorProfile) -> bool:
        """Apply persona behavior profile to personality engine"""
        self.persona_behavior = persona_behavior
        
        self.enthusiasm_level = max(0.0, min(1.0, 
            self.enthusiasm_level * (1.0 + (persona_behavior.enthusiasm - 0.5) * 0.4)
        ))
        self.playfulness = max(0.0, min(1.0,
            self.playfulness * (1.0 + (persona_behavior.humor - 0.5) * 0.4)
        ))
        self.professionalism = max(0.0, min(1.0,
            self.professionalism * (1.0 + (persona_behavior.formality - 0.5) * 0.4)
        ))
        
        return True
    
    def get_persona_modifiers(self) -> Dict[str, float]:
        """Get personality trait modifiers from persona"""
        if not self.persona_behavior:
            return {
                "enthusiasm": 1.0,
                "warmth": 1.0,
                "humor": 1.0,
                "formality": 1.0,
                "empathy": 1.0
            }
        
        return {
            "enthusiasm": self.persona_behavior.enthusiasm,
            "warmth": self.persona_behavior.warmth,
            "humor": self.persona_behavior.humor,
            "formality": self.persona_behavior.formality,
            "empathy": self.persona_behavior.empathy
        }
