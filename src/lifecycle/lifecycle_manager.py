"""
Lifecycle & State Manager Module
Manages AI birth, growth, and lifecycle tied to phone power
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
from enum import Enum
from src.types import PermissionGrant, PermissionType


class AILifecycleStage(Enum):
    """AI lifecycle stages"""
    BIRTH = "birth"              # Just installed
    INITIALIZATION = "init"      # Setting up permissions
    EARLY_LEARNING = "early_learning"  # Learning from first interactions
    GROWTH = "growth"            # Established, learning actively
    MATURE = "mature"            # Fully bonded, personalized
    DORMANT = "dormant"          # Phone is off/inactive
    END_OF_LIFE = "end_of_life"  # Phone dying or uninstall


class LifecycleManager:
    """
    Manages the AI's lifecycle from birth to end of life.
    Tracks state, permissions, and milestones.
    """
    
    def __init__(self):
        self.current_stage = AILifecycleStage.BIRTH
        self.birth_time = datetime.now()
        self.last_active_time = datetime.now()
        self.runtime_seconds = 0
        
        # Permissions
        self.permissions: Dict[PermissionType, PermissionGrant] = self._init_permissions()
        
        # Milestones
        self.milestones_reached: Dict[str, datetime] = {}
        self.interaction_count = 0
        self.days_active = 0
        
        # Full AI Mode state
        self.full_ai_mode_enabled = False
        self.full_ai_mode_activated_time: Optional[datetime] = None
        
        # Background state
        self.background_monitoring_active = False
        self.is_charging = False
        self.battery_percent = 100
    
    def _init_permissions(self) -> Dict[PermissionType, PermissionGrant]:
        """Initialize permissions (all denied by default)"""
        return {
            permission: PermissionGrant(permission=permission, granted=False, explicit_consent=False)
            for permission in PermissionType
        }
    
    def on_birth(self):
        """Called when AI is first installed"""
        self.birth_time = datetime.now()
        self.last_active_time = datetime.now()
        self.current_stage = AILifecycleStage.INITIALIZATION
        self._record_milestone("birth")
    
    def request_permission(self, permission: PermissionType, 
                          user_approved: bool = False) -> bool:
        """Request user permission"""
        if permission in self.permissions:
            grant = self.permissions[permission]
            if user_approved:
                grant.granted = True
                grant.explicit_consent = True
                grant.granted_at = datetime.now()
                
                # Check if full AI mode now possible
                if permission == PermissionType.FULL_AI_MODE:
                    self._check_full_ai_mode_available()
                
                return True
        
        return False
    
    def revoke_permission(self, permission: PermissionType):
        """Revoke user permission"""
        if permission in self.permissions:
            grant = self.permissions[permission]
            grant.granted = False
            grant.revoked_at = datetime.now()
            
            if permission == PermissionType.FULL_AI_MODE:
                self.full_ai_mode_enabled = False
    
    def enable_full_ai_mode(self) -> bool:
        """Enable Full AI Mode if all permissions granted"""
        # Require explicit permission
        if not self.permissions[PermissionType.FULL_AI_MODE].granted:
            return False
        
        self.full_ai_mode_enabled = True
        self.full_ai_mode_activated_time = datetime.now()
        self._record_milestone("full_ai_mode_enabled")
        
        return True
    
    def disable_full_ai_mode(self):
        """Disable Full AI Mode"""
        self.full_ai_mode_enabled = False
    
    def _check_full_ai_mode_available(self):
        """Check if Full AI Mode can be enabled"""
        # Require microphone, camera, sensors, and full_ai_mode permission
        required = [
            PermissionType.MICROPHONE,
            PermissionType.CAMERA,
            PermissionType.SENSORS,
            PermissionType.FULL_AI_MODE
        ]
        
        all_granted = all(
            self.permissions[p].granted for p in required
        )
        
        if all_granted:
            self._record_milestone("full_ai_mode_available")
    
    def on_interaction(self):
        """Called when user interacts with AI"""
        self.last_active_time = datetime.now()
        self.interaction_count += 1
        self._check_stage_progression()
    
    def on_phone_active(self):
        """Called when phone wakes up"""
        self.last_active_time = datetime.now()
        if self.current_stage == AILifecycleStage.DORMANT:
            self.current_stage = AILifecycleStage.GROWTH
    
    def on_phone_sleep(self):
        """Called when phone goes to sleep"""
        if self.full_ai_mode_enabled and self.background_monitoring_active:
            # Continue background monitoring
            pass
        else:
            self.current_stage = AILifecycleStage.DORMANT
    
    def on_charging(self, is_charging: bool):
        """Called when charging state changes"""
        self.is_charging = is_charging
    
    def on_battery_update(self, battery_percent: float):
        """Called when battery level updates"""
        self.battery_percent = battery_percent
    
    def _check_stage_progression(self):
        """Check if AI should progress to next lifecycle stage"""
        time_active = (datetime.now() - self.birth_time).total_seconds()
        self.runtime_seconds = int(time_active)
        self.days_active = int(time_active / 86400)
        
        # Progression rules
        if self.current_stage == AILifecycleStage.INITIALIZATION:
            if self.interaction_count > 5:
                self.current_stage = AILifecycleStage.EARLY_LEARNING
                self._record_milestone("early_learning_started")
        
        elif self.current_stage == AILifecycleStage.EARLY_LEARNING:
            if self.interaction_count > 50 or self.days_active >= 1:
                self.current_stage = AILifecycleStage.GROWTH
                self._record_milestone("growth_stage_reached")
        
        elif self.current_stage == AILifecycleStage.GROWTH:
            # Move to mature stage after significant bonding
            if self.interaction_count > 500 or self.days_active >= 7:
                self.current_stage = AILifecycleStage.MATURE
                self._record_milestone("maturity_reached")
    
    def _record_milestone(self, milestone: str):
        """Record achievement of milestone"""
        if milestone not in self.milestones_reached:
            self.milestones_reached[milestone] = datetime.now()
    
    def on_phone_shutdown(self):
        """Called when phone is shutting down"""
        self._record_milestone("last_active")
    
    def on_uninstall(self):
        """Called when AI is being uninstalled"""
        self.current_stage = AILifecycleStage.END_OF_LIFE
        self._record_milestone("end_of_life")
    
    def is_in_background_mode(self) -> bool:
        """Check if AI can operate in background"""
        return (
            self.full_ai_mode_enabled and
            self.permissions[PermissionType.BACKGROUND_MONITORING].granted
        )
    
    def get_lifecycle_status(self) -> Dict[str, any]:
        """Get comprehensive lifecycle status"""
        return {
            "stage": self.current_stage.value,
            "birth_time": self.birth_time.isoformat(),
            "last_active": self.last_active_time.isoformat(),
            "runtime_seconds": self.runtime_seconds,
            "days_active": self.days_active,
            "interactions": self.interaction_count,
            "full_ai_mode": {
                "enabled": self.full_ai_mode_enabled,
                "activated_at": self.full_ai_mode_activated_time.isoformat() if self.full_ai_mode_activated_time else None
            },
            "background_monitoring": self.background_monitoring_active,
            "phone_state": {
                "is_charging": self.is_charging,
                "battery_percent": self.battery_percent
            },
            "permissions": {
                perm.name: {
                    "granted": grant.granted,
                    "explicit_consent": grant.explicit_consent,
                    "granted_at": grant.granted_at.isoformat() if grant.granted_at else None
                }
                for perm, grant in self.permissions.items()
            },
            "milestones": {
                milestone: timestamp.isoformat()
                for milestone, timestamp in self.milestones_reached.items()
            }
        }
    
    def get_startup_message(self) -> str:
        """Get appropriate startup message"""
        if self.current_stage == AILifecycleStage.BIRTH:
            return "Hello! I'm Project Mind, your new AI companion. Let's get to know each other!"
        elif self.current_stage == AILifecycleStage.INITIALIZATION:
            return "Welcome back! I'd love to ask for some permissions to help you better."
        elif self.current_stage == AILifecycleStage.EARLY_LEARNING:
            return f"Good to see you again! I've been learning from our conversations."
        elif self.current_stage == AILifecycleStage.GROWTH:
            return f"Hey! I've been growing and evolving. I feel like I know you better now!"
        elif self.current_stage == AILifecycleStage.MATURE:
            return f"My friend, it's wonderful to be with you again. Let's continue our journey together."
        else:
            return "I'm here for you. What do you need?"
