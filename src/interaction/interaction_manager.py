"""
Interaction Manager Module
Handles voice, text, and gesture interactions with the user
"""

from datetime import datetime
from typing import Dict, List, Optional, Callable
from src.types import InteractionLog, PermissionType


class InteractionManager:
    """
    Manages all interactions between user and AI.
    Handles text, voice, and touch-based interactions.
    """
    
    def __init__(self):
        self.interaction_history: List[InteractionLog] = []
        self.pending_responses: Dict[str, str] = {}
        self.notification_queue: List[Dict] = []
        
        # Callbacks for different interaction types
        self.voice_handler: Optional[Callable] = None
        self.text_handler: Optional[Callable] = None
        self.gesture_handler: Optional[Callable] = None
    
    def handle_text_input(self, text: str, context: Optional[Dict] = None) -> str:
        """Handle text input from user"""
        log_entry = InteractionLog(
            timestamp=datetime.now(),
            interaction_type="text",
            content=text,
            ai_response="",
            context=context or {}
        )
        
        # Process text (in production, would go to LLM)
        response = self._generate_response(text, "text")
        log_entry.ai_response = response
        
        self.interaction_history.append(log_entry)
        return response
    
    def handle_voice_input(self, transcript: str, audio_features: Optional[Dict] = None) -> str:
        """Handle voice input"""
        context = {
            "audio_features": audio_features or {},
            "voice_detected": True
        }
        
        log_entry = InteractionLog(
            timestamp=datetime.now(),
            interaction_type="voice",
            content=transcript,
            ai_response="",
            context=context
        )
        
        # Detect emotion from voice
        if audio_features:
            emotion = self._detect_emotion_from_audio(audio_features)
            log_entry.emotion_detected = emotion
        
        response = self._generate_response(transcript, "voice")
        log_entry.ai_response = response
        
        self.interaction_history.append(log_entry)
        return response
    
    def handle_gesture(self, gesture_type: str) -> Optional[str]:
        """Handle touch/gesture input"""
        gestures = {
            "swipe_up": "user_scrolling",
            "swipe_down": "user_scrolling",
            "double_tap": "user_attention",
            "long_press": "user_context_menu",
            "shake": "user_device_shake"
        }
        
        if gesture_type in gestures:
            log_entry = InteractionLog(
                timestamp=datetime.now(),
                interaction_type="gesture",
                content=gesture_type,
                ai_response="",
                context={"gesture_action": gestures[gesture_type]}
            )
            self.interaction_history.append(log_entry)
            
            # Handle specific gestures
            if gesture_type == "shake":
                return self._handle_shake_gesture()
        
        return None
    
    def _detect_emotion_from_audio(self, audio_features: Dict) -> Optional[str]:
        """Detect emotion from voice features"""
        # Simple heuristic (in production, would use ML model)
        pitch = audio_features.get("pitch", 0)
        energy = audio_features.get("energy", 0)
        
        if energy > 0.8:
            return "excited" if pitch > 150 else "angry"
        elif energy < 0.3:
            return "calm" if pitch < 100 else "sad"
        else:
            return "neutral"
    
    def _generate_response(self, input_text: str, interaction_type: str) -> str:
        """Generate response (placeholder)"""
        # In production, would call LLM
        response_templates = {
            "text": f"I understand you said: '{input_text[:50]}...'. How can I help?",
            "voice": f"I heard you say: '{input_text[:50]}...'. Tell me more!",
            "gesture": "You interacted with me!"
        }
        return response_templates.get(interaction_type, "How can I assist you?")
    
    def _handle_shake_gesture(self) -> str:
        """Handle device shake"""
        return "I felt that shake! Are you okay? Do you need help?"
    
    def add_notification(self, title: str, message: str, priority: str = "normal"):
        """Add notification to queue"""
        notification = {
            "id": f"notif_{len(self.notification_queue)}_{datetime.now().timestamp()}",
            "title": title,
            "message": message,
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
            "delivered": False
        }
        self.notification_queue.append(notification)
        return notification["id"]
    
    def mark_notification_delivered(self, notification_id: str):
        """Mark notification as delivered to user"""
        for notif in self.notification_queue:
            if notif["id"] == notification_id:
                notif["delivered"] = True
                break
    
    def get_pending_notifications(self) -> List[Dict]:
        """Get undelivered notifications"""
        return [n for n in self.notification_queue if not n["delivered"]]
    
    def get_recent_interactions(self, limit: int = 10) -> List[InteractionLog]:
        """Get recent interactions"""
        return self.interaction_history[-limit:]
    
    def get_interaction_stats(self) -> Dict[str, any]:
        """Get interaction statistics"""
        if not self.interaction_history:
            return {
                "total_interactions": 0,
                "by_type": {},
                "avg_response_time_ms": 0
            }
        
        by_type = {}
        for interaction in self.interaction_history:
            by_type[interaction.interaction_type] = (
                by_type.get(interaction.interaction_type, 0) + 1
            )
        
        # Calculate average response time (time between interaction and response)
        response_times = []
        for interaction in self.interaction_history[-100:]:
            # Simplified: would need actual timing in production
            response_times.append(100)  # Mock 100ms
        
        avg_response_time = (
            sum(response_times) / len(response_times) if response_times else 0
        )
        
        return {
            "total_interactions": len(self.interaction_history),
            "by_type": by_type,
            "avg_response_time_ms": avg_response_time,
            "notifications_sent": len(self.notification_queue),
            "pending_notifications": len(self.get_pending_notifications())
        }
    
    def set_voice_handler(self, handler: Callable):
        """Set handler for voice interactions"""
        self.voice_handler = handler
    
    def set_text_handler(self, handler: Callable):
        """Set handler for text interactions"""
        self.text_handler = handler
    
    def set_gesture_handler(self, handler: Callable):
        """Set handler for gesture interactions"""
        self.gesture_handler = handler
    
    def clear_history(self):
        """Clear interaction history"""
        self.interaction_history.clear()
    
    def export_interactions(self, limit: int = 100) -> List[Dict]:
        """Export interactions in readable format"""
        return [
            {
                "timestamp": i.timestamp.isoformat(),
                "type": i.interaction_type,
                "user_input": i.content[:100],
                "ai_response": i.ai_response[:100],
                "context": i.context
            }
            for i in self.interaction_history[-limit:]
        ]
