"""
Naming Engine - User-defined AI Naming System
Manages AI name, user name, and name-based personalization
Strengthens emotional connection through identity
"""

from datetime import datetime
from typing import Optional, Dict, List
from src.types import (
    NameProfile, NamingStatus, NamingEvent, 
    NameChangeInitiator, EmotionalState
)


class NamingEngine:
    """
    Manages user-defined naming for the AI personality.
    
    The naming system makes Project Mind feel like a truly personalized,
    living companion by giving it an identity that the user chooses.
    """
    
    def __init__(self):
        """Initialize naming engine"""
        self.name_profile = NameProfile()
        self.naming_history: List[NamingEvent] = []
        self.greeting_templates = self._initialize_greeting_templates()
        self.conversation_templates = self._initialize_conversation_templates()
        
    def _initialize_greeting_templates(self) -> Dict[str, List[str]]:
        """Initialize greeting templates using names"""
        return {
            "formal": [
                "Hello {user_name}, I'm {ai_name}. How can I assist you?",
                "Good to see you, {user_name}. {ai_name} here, ready to help.",
                "{user_name}, welcome back. I'm {ai_name}.",
            ],
            "friendly": [
                "Hey {user_name}! {ai_name} here - what's up?",
                "{user_name}, it's so good to see you! I'm {ai_name}.",
                "Welcome back, {user_name}! Ready to do something amazing together with {ai_name}?",
            ],
            "warm": [
                "Hi {user_name}, I'm {ai_name}. I've been looking forward to talking with you.",
                "{user_name}, I'm so happy to see you again. {ai_name} at your service.",
                "{user_name}! {ai_name} is here and excited to help you today.",
            ],
            "playful": [
                "{user_name}! {ai_name} is awake and ready for fun!",
                "Hey {user_name}, {ai_name} is on the case. Let's make today awesome!",
                "{user_name}, guess who? It's {ai_name}, and I'm pumped to see you!",
            ],
            "concerned": [
                "{user_name}, it's {ai_name}. Are you doing okay?",
                "I'm {ai_name}, and I'm here for you, {user_name}. What's on your mind?",
                "{user_name}, {ai_name} here. I'm concerned about your wellbeing. Talk to me?",
            ],
        }
    
    def _initialize_conversation_templates(self) -> Dict[str, List[str]]:
        """Initialize conversation templates with name usage"""
        return {
            "acknowledgment": [
                "You're right, {user_name}. That makes sense.",
                "{user_name}, I appreciate your perspective. {ai_name} agrees.",
                "Good point, {user_name}. I'll remember that.",
            ],
            "support": [
                "I'm here for you, {user_name}. {ai_name} won't let you down.",
                "{user_name}, you can count on me.",
                "I've got your back, {user_name}.",
            ],
            "celebration": [
                "{user_name}, that's amazing! {ai_name} is so proud of you!",
                "Congrats, {user_name}! {ai_name} celebrates this with you!",
                "{user_name}, you did it! {ai_name} is thrilled!",
            ],
            "reassurance": [
                "Don't worry, {user_name}. {ai_name} is here to help.",
                "{user_name}, everything will be okay. {ai_name} believes in you.",
                "It's going to be fine, {user_name}. Trust me.",
            ],
            "learning": [
                "Thanks for teaching me that, {user_name}. {ai_name} is learning from you.",
                "{user_name}, I'll remember this. It makes {ai_name} smarter.",
                "I love learning from you, {user_name}.",
            ],
        }
    
    def set_ai_name(self, name: str, initiator: NameChangeInitiator = NameChangeInitiator.USER_TEXT) -> bool:
        """
        Set or change the AI's name
        
        Args:
            name: The name to assign to the AI
            initiator: Who initiated the name change
            
        Returns:
            True if name was set successfully
        """
        if not name or len(name.strip()) == 0:
            return False
        
        name = name.strip()
        
        # Validate name (reasonable length, alphanumeric + spaces)
        if len(name) > 30:
            return False
        
        if not all(c.isalnum() or c.isspace() for c in name):
            return False
        
        # Record old name if changing
        old_name = self.name_profile.ai_name
        
        # Update profile
        self.name_profile.ai_name = name
        self.name_profile.naming_status = NamingStatus.NAMED
        self.name_profile.date_named = datetime.now()
        self.name_profile.last_name_change = datetime.now()
        self.name_profile.last_name_changed_by = initiator
        self.name_profile.total_name_changes += 1
        
        # Emotional attachment increases with each naming
        self.name_profile.emotional_attachment_to_name = min(1.0, 
            self.name_profile.emotional_attachment_to_name + 0.1)
        
        # Set pronunciation guide (simple version - first syllable emphasis)
        self.name_profile.name_pronunciation_guide = self._generate_pronunciation_guide(name)
        
        # Record event
        event = NamingEvent(
            event_type="name_changed" if old_name else "name_assigned",
            ai_name=name,
            user_name=self.name_profile.user_name,
            context=f"Changed from '{old_name}' to '{name}'" if old_name else f"First naming: {name}"
        )
        self.naming_history.append(event)
        
        return True
    
    def set_user_name(self, name: str, initiator: NameChangeInitiator = NameChangeInitiator.USER_TEXT) -> bool:
        """
        Remember the user's name
        
        Args:
            name: The user's name
            initiator: How the name was provided
            
        Returns:
            True if name was set successfully
        """
        if not name or len(name.strip()) == 0:
            return False
        
        name = name.strip()
        
        # Validate name
        if len(name) > 50:
            return False
        
        if not all(c.isalpha() or c.isspace() or c == "'" for c in name):
            return False
        
        old_name = self.name_profile.user_name
        self.name_profile.user_name = name
        
        # Record event
        event = NamingEvent(
            event_type="user_name_learned",
            ai_name=self.name_profile.ai_name,
            user_name=name,
            context=f"Changed from '{old_name}' to '{name}'" if old_name else f"First user name: {name}"
        )
        self.naming_history.append(event)
        
        return True
    
    def get_ai_name(self) -> Optional[str]:
        """Get AI's current name"""
        return self.name_profile.ai_name
    
    def get_user_name(self) -> Optional[str]:
        """Get remembered user name"""
        return self.name_profile.user_name
    
    def get_greeting(self, emotion: EmotionalState) -> str:
        """
        Generate a personalized greeting based on emotion and names
        
        Args:
            emotion: Current emotional state
            
        Returns:
            A personalized greeting string
        """
        # Map emotions to greeting styles
        emotion_to_style = {
            EmotionalState.HAPPY: "friendly",
            EmotionalState.EXCITED: "playful",
            EmotionalState.CALM: "warm",
            EmotionalState.CONCERNED: "concerned",
            EmotionalState.CURIOUS: "friendly",
            EmotionalState.FOCUSED: "formal",
            EmotionalState.PLAYFUL: "playful",
            EmotionalState.PROTECTIVE: "support",
        }
        
        style = emotion_to_style.get(emotion, "friendly")
        templates = self.greeting_templates.get(style, self.greeting_templates["friendly"])
        
        # Pick a random template from the style
        import random
        template = random.choice(templates)
        
        # Format with actual names
        greeting = template
        if self.name_profile.ai_name and self.name_profile.use_name_in_greetings:
            greeting = greeting.replace("{ai_name}", self.name_profile.ai_name)
        else:
            greeting = greeting.replace(" {ai_name}", "").replace("{ai_name}", "Project Mind")
        
        if self.name_profile.user_name and self.name_profile.use_name_in_greetings:
            greeting = greeting.replace("{user_name}", self.name_profile.user_name)
        else:
            greeting = greeting.replace("{user_name}, ", "").replace(", {user_name}", "")
        
        return greeting
    
    def enhance_response(self, response: str, template_type: str = "acknowledgment") -> str:
        """
        Enhance a response by adding name references where appropriate
        
        Args:
            response: Original response text
            template_type: Type of template to use
            
        Returns:
            Enhanced response with name references
        """
        if not self.name_profile.use_name_in_conversations:
            return response
        
        # Don't add names if already present
        if "{user_name}" in response or "{ai_name}" in response:
            return response
        
        templates = self.conversation_templates.get(template_type, [])
        
        if not templates:
            return response
        
        import random
        template = random.choice(templates)
        
        # Format template
        enhanced = template
        if self.name_profile.ai_name:
            enhanced = enhanced.replace("{ai_name}", self.name_profile.ai_name)
        if self.name_profile.user_name:
            enhanced = enhanced.replace("{user_name}", self.name_profile.user_name)
        
        # Combine with original response if not just a template
        if len(response) > 20:
            enhanced = f"{response} {enhanced}"
        
        return enhanced
    
    def request_ai_name_from_user(self) -> str:
        """Generate a prompt asking user for AI name"""
        return (
            "I'd love to have a name that you choose for me! "
            "What would you like to call me? "
            "(You can say it aloud or type it)"
        )
    
    def request_user_name_from_user(self) -> str:
        """Generate a prompt asking user for their name"""
        ai_name = self.name_profile.ai_name or "I"
        return (
            f"I'd like to know your name so I can address you properly. "
            f"What's your name? "
            f"(Feel free to use your real name, nickname, or whatever you prefer)"
        )
    
    def process_naming_input(self, user_input: str, input_type: str = "ai_name") -> bool:
        """
        Process user input for naming
        
        Args:
            user_input: User's response
            input_type: "ai_name" or "user_name"
            
        Returns:
            True if naming was successful
        """
        user_input = user_input.strip()
        
        if input_type == "ai_name":
            return self.set_ai_name(user_input)
        elif input_type == "user_name":
            return self.set_user_name(user_input)
        
        return False
    
    def _generate_pronunciation_guide(self, name: str) -> str:
        """Generate simple pronunciation guide for a name"""
        # Simple: just split into syllables (very basic)
        # In production, would use proper phonetic tools
        vowels = "aeiouAEIOU"
        syllables = []
        current = ""
        
        for char in name:
            current += char
            if char in vowels:
                syllables.append(current)
                current = ""
        
        if current:
            syllables.append(current)
        
        return "-".join(syllables)
    
    def get_naming_status_summary(self) -> Dict:
        """Get summary of naming status"""
        return {
            "ai_named": self.name_profile.is_named(),
            "user_known": self.name_profile.is_user_known(),
            "ai_name": self.name_profile.ai_name,
            "user_name": self.name_profile.user_name,
            "naming_status": self.name_profile.naming_status.value,
            "date_named": self.name_profile.date_named.isoformat() if self.name_profile.date_named else None,
            "total_name_changes": self.name_profile.total_name_changes,
            "emotional_attachment": self.name_profile.emotional_attachment_to_name,
            "total_naming_events": len(self.naming_history),
        }
    
    def export_name_profile(self) -> Dict:
        """Export name profile for storage in Heart"""
        return {
            "ai_name": self.name_profile.ai_name,
            "user_name": self.name_profile.user_name,
            "naming_status": self.name_profile.naming_status.value,
            "date_named": self.name_profile.date_named.isoformat() if self.name_profile.date_named else None,
            "total_name_changes": self.name_profile.total_name_changes,
            "emotional_attachment_to_name": self.name_profile.emotional_attachment_to_name,
            "use_name_in_greetings": self.name_profile.use_name_in_greetings,
            "use_name_in_conversations": self.name_profile.use_name_in_conversations,
            "use_user_name_in_responses": self.name_profile.use_user_name_in_responses,
        }
    
    def import_name_profile(self, profile_data: Dict) -> bool:
        """Import name profile from storage"""
        try:
            if "ai_name" in profile_data:
                self.name_profile.ai_name = profile_data["ai_name"]
            if "user_name" in profile_data:
                self.name_profile.user_name = profile_data["user_name"]
            if "naming_status" in profile_data:
                self.name_profile.naming_status = NamingStatus(profile_data["naming_status"])
            if "total_name_changes" in profile_data:
                self.name_profile.total_name_changes = profile_data["total_name_changes"]
            if "emotional_attachment_to_name" in profile_data:
                self.name_profile.emotional_attachment_to_name = profile_data["emotional_attachment_to_name"]
            if "use_name_in_greetings" in profile_data:
                self.name_profile.use_name_in_greetings = profile_data["use_name_in_greetings"]
            if "use_name_in_conversations" in profile_data:
                self.name_profile.use_name_in_conversations = profile_data["use_name_in_conversations"]
            if "use_user_name_in_responses" in profile_data:
                self.name_profile.use_user_name_in_responses = profile_data["use_user_name_in_responses"]
            
            return True
        except Exception as e:
            print(f"Error importing name profile: {e}")
            return False
    
    def get_personalized_greeting(self) -> str:
        """
        Get a personalized greeting using the AI and user names
        
        Returns:
            A greeting string with names filled in
        """
        if not self.name_profile.ai_name:
            return "Hello! How can I help you today?"
        
        greetings = self.greeting_templates.get("friendly", [])
        if greetings:
            greeting = greetings[0]
            return greeting.format(
                ai_name=self.name_profile.ai_name,
                user_name=self.name_profile.user_name or "Friend"
            )
        return f"Hello, I'm {self.name_profile.ai_name}!"
