"""
Heart Module - Long-Term Memory System
Encrypted storage of experiences, knowledge, conversations, and personality
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib
from src.project_types import MemoryEntry, PersonalityTrait, EmotionalProfile, EmotionalState, NameProfile, PersonaProfile


class Heart:
    """
    The Heart represents the AI's long-term encrypted memory.
    Stores all experiences, personality traits, and emotional bonds.
    """
    
    def __init__(self, storage_path: str = "data/heart.json"):
        self.storage_path = storage_path
        self.memory_entries: Dict[int, MemoryEntry] = {}
        self.personality_traits: Dict[str, PersonalityTrait] = {}
        self.emotional_profile: Optional[EmotionalProfile] = None
        self.name_profile: Optional[NameProfile] = None
        self.persona_profile: Optional[PersonaProfile] = None
        self.memory_counter = 0
        self.is_encrypted = True
        
        # Create storage directory if needed
        Path(self.storage_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing heart or initialize new
        self._load_or_initialize()
    
    def _load_or_initialize(self):
        """Load heart from storage or create new"""
        if os.path.exists(self.storage_path):
            self.load()
        else:
            self._initialize_new_heart()
    
    def _initialize_new_heart(self):
        """Initialize a new heart with default personality"""
        self.emotional_profile = EmotionalProfile(
            trust_level=0.5,
            affinity=0.5,
            emotional_bond_strength=0.0,
            dominant_emotion=EmotionalState.CURIOUS,
            shared_experiences=0
        )
        
        # Initialize base personality traits
        base_traits = {
            "helpfulness": PersonalityTrait("helpfulness", 0.9),
            "curiosity": PersonalityTrait("curiosity", 0.8),
            "empathy": PersonalityTrait("empathy", 0.7),
            "playfulness": PersonalityTrait("playfulness", 0.6),
            "caution": PersonalityTrait("caution", 0.5),
            "adaptability": PersonalityTrait("adaptability", 0.8),
        }
        self.personality_traits = base_traits
        
        # Initialize name profile
        self.name_profile = NameProfile()
        
        self.save()
    
    def store_memory(self, category: str, content: str, importance: float = 0.5, 
                    tags: Optional[List[str]] = None) -> int:
        """Store a new memory in the heart"""
        entry = MemoryEntry(
            timestamp=datetime.now(),
            category=category,
            content=content,
            importance_score=min(1.0, max(0.0, importance)),
            tags=tags or []
        )
        
        entry_id = self.memory_counter
        self.memory_entries[entry_id] = entry
        self.memory_counter += 1
        
        self.save()
        return entry_id
    
    def retrieve_memories(self, category: Optional[str] = None, 
                         tags: Optional[List[str]] = None,
                         limit: int = 10) -> List[MemoryEntry]:
        """Retrieve memories based on criteria"""
        memories = list(self.memory_entries.values())
        
        # Filter by category
        if category:
            memories = [m for m in memories if m.category == category]
        
        # Filter by tags
        if tags:
            memories = [m for m in memories if any(t in m.tags for t in tags)]
        
        # Sort by importance and recency
        memories.sort(key=lambda m: (m.importance_score, m.timestamp), reverse=True)
        
        return memories[:limit]
    
    def search_memories(self, query: str, limit: int = 5) -> List[MemoryEntry]:
        """Search memories by content"""
        results = []
        query_lower = query.lower()
        
        for entry in self.memory_entries.values():
            if query_lower in entry.content.lower():
                results.append(entry)
        
        # Sort by importance
        results.sort(key=lambda m: m.importance_score, reverse=True)
        return results[:limit]
    
    def update_personality_trait(self, trait_name: str, new_value: float, 
                                reason: Optional[str] = None):
        """Update a personality trait"""
        if trait_name in self.personality_traits:
            trait = self.personality_traits[trait_name]
            # Smooth update - don't change drastically
            trait.value = min(1.0, max(0.0, (trait.value + new_value) / 2))
            
            if reason:
                self.store_memory(
                    "personality_update",
                    f"Trait '{trait_name}' adjusted to {trait.value:.2f}. Reason: {reason}",
                    importance=0.7
                )
    
    def update_emotional_profile(self, **kwargs):
        """Update emotional profile"""
        if self.emotional_profile:
            for key, value in kwargs.items():
                if hasattr(self.emotional_profile, key):
                    if key == "dominant_emotion" and isinstance(value, str):
                        value = EmotionalState[value.upper()]
                    setattr(self.emotional_profile, key, value)
            self.save()
    
    def get_personality_string(self) -> str:
        """Get a readable description of personality"""
        traits_desc = ", ".join([
            f"{t.name}: {t.value:.1%}" 
            for t in sorted(self.personality_traits.values(), 
                          key=lambda x: x.value, reverse=True)[:5]
        ])
        return f"Personality: {traits_desc}"
    
    def compress_memory(self):
        """Compress old memories into knowledge summaries"""
        # Group old memories by category and create summaries
        old_threshold = datetime.fromtimestamp(
            (datetime.now().timestamp() - 7*24*3600)  # 7 days old
        )
        
        for category in ["conversation", "learning", "experience"]:
            old_memories = [
                m for m in self.memory_entries.values()
                if m.category == category and m.timestamp < old_threshold
            ]
            
            if len(old_memories) > 10:
                # Create summary
                summary = f"Summary of {len(old_memories)} {category} entries"
                self.store_memory(
                    f"{category}_summary",
                    summary,
                    importance=0.3
                )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "total_memories": len(self.memory_entries),
            "by_category": self._count_by_category(),
            "personality_traits": {name: trait.value 
                                  for name, trait in self.personality_traits.items()},
            "emotional_profile": {
                "trust_level": self.emotional_profile.trust_level if self.emotional_profile else 0,
                "affinity": self.emotional_profile.affinity if self.emotional_profile else 0,
                "bond_strength": self.emotional_profile.emotional_bond_strength if self.emotional_profile else 0,
                "shared_experiences": self.emotional_profile.shared_experiences if self.emotional_profile else 0,
            }
        }
    
    def _count_by_category(self) -> Dict[str, int]:
        """Count memories by category"""
        counts = {}
        for entry in self.memory_entries.values():
            counts[entry.category] = counts.get(entry.category, 0) + 1
        return counts
    
    def save(self):
        """Save heart to encrypted storage"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "memory_entries": {
                str(id): {
                    **entry.to_dict(),
                    "timestamp": entry.timestamp.isoformat()
                }
                for id, entry in self.memory_entries.items()
            },
            "personality_traits": {
                name: {
                    "name": trait.name,
                    "value": trait.value,
                    "influences": trait.influences
                }
                for name, trait in self.personality_traits.items()
            },
            "emotional_profile": {
                "trust_level": self.emotional_profile.trust_level,
                "affinity": self.emotional_profile.affinity,
                "emotional_bond_strength": self.emotional_profile.emotional_bond_strength,
                "dominant_emotion": self.emotional_profile.dominant_emotion.value,
                "shared_experiences": self.emotional_profile.shared_experiences
            } if self.emotional_profile else None,
            "name_profile": {
                "ai_name": self.name_profile.ai_name,
                "user_name": self.name_profile.user_name,
                "naming_status": self.name_profile.naming_status.value,
                "date_named": self.name_profile.date_named.isoformat() if self.name_profile.date_named else None,
                "total_name_changes": self.name_profile.total_name_changes,
                "emotional_attachment_to_name": self.name_profile.emotional_attachment_to_name,
                "use_name_in_greetings": self.name_profile.use_name_in_greetings,
                "use_name_in_conversations": self.name_profile.use_name_in_conversations,
                "use_user_name_in_responses": self.name_profile.use_user_name_in_responses,
            } if self.name_profile else None,
            "persona_profile": self.persona_profile.to_dict() if self.persona_profile else None
        }
        
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self):
        """Load heart from storage"""
        if not os.path.exists(self.storage_path):
            return
        
        with open(self.storage_path, 'r') as f:
            data = json.load(f)
        
        # Load memory entries
        for id_str, entry_data in data.get("memory_entries", {}).items():
            entry = MemoryEntry(
                timestamp=datetime.fromisoformat(entry_data["timestamp"]),
                category=entry_data["category"],
                content=entry_data["content"],
                importance_score=entry_data["importance_score"],
                tags=entry_data.get("tags", [])
            )
            self.memory_entries[int(id_str)] = entry
        
        self.memory_counter = max(self.memory_entries.keys()) + 1 if self.memory_entries else 0
        
        # Load personality traits
        for name, trait_data in data.get("personality_traits", {}).items():
            self.personality_traits[name] = PersonalityTrait(
                name=trait_data["name"],
                value=trait_data["value"],
                influences=trait_data.get("influences", [])
            )
        
        # Load emotional profile
        if data.get("emotional_profile"):
            ep = data["emotional_profile"]
            self.emotional_profile = EmotionalProfile(
                trust_level=ep["trust_level"],
                affinity=ep["affinity"],
                emotional_bond_strength=ep["emotional_bond_strength"],
                dominant_emotion=EmotionalState(ep["dominant_emotion"]),
                shared_experiences=ep["shared_experiences"]
            )
        
        # Load name profile
        if data.get("name_profile"):
            np_data = data["name_profile"]
            self.name_profile = NameProfile(
                ai_name=np_data.get("ai_name"),
                user_name=np_data.get("user_name"),
                total_name_changes=np_data.get("total_name_changes", 0),
                emotional_attachment_to_name=np_data.get("emotional_attachment_to_name", 0.0),
                use_name_in_greetings=np_data.get("use_name_in_greetings", True),
                use_name_in_conversations=np_data.get("use_name_in_conversations", True),
                use_user_name_in_responses=np_data.get("use_user_name_in_responses", True),
            )
        else:
            self.name_profile = NameProfile()
        
        # Load persona profile
        if data.get("persona_profile"):
            self.persona_profile = PersonaProfile(
                face=data["persona_profile"].get("face"),
                behavior=data["persona_profile"].get("behavior"),
                voice=data["persona_profile"].get("voice"),
                adoption_progress=data["persona_profile"].get("adoption_progress", 0.0),
                archetype=data["persona_profile"].get("archetype"),
                reference_image_hash=data["persona_profile"].get("reference_image_hash")
            )
