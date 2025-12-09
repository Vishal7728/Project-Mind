"""
Working Memory (RAM) Module
Fast temporary processing for reasoning and problem solving
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Deque
from collections import deque
from src.types import InteractionLog, SensorData


class WorkingMemory:
    """
    Working Memory represents the AI's temporary RAM.
    Used for fast reasoning, searches, and problem-solving (<1 second retrieval).
    Automatically purges old data to optimize performance.
    """
    
    def __init__(self, max_entries: int = 1000, retention_seconds: int = 3600):
        self.max_entries = max_entries
        self.retention_seconds = retention_seconds
        
        # Fast access caches
        self.recent_interactions: Deque[InteractionLog] = deque(maxlen=100)
        self.sensor_cache: Dict[str, SensorData] = {}
        self.reasoning_cache: Dict[str, Any] = {}
        self.context_state: Dict[str, Any] = {}
        
        # Performance tracking
        self.cache_hits = 0
        self.cache_misses = 0
    
    def store_interaction(self, interaction: InteractionLog):
        """Store interaction in working memory"""
        self.recent_interactions.append(interaction)
        self._purge_old_data()
    
    def store_sensor_data(self, sensor_name: str, data: SensorData):
        """Store sensor reading for fast access"""
        self.sensor_cache[sensor_name] = data
    
    def get_recent_interactions(self, limit: int = 10) -> List[InteractionLog]:
        """Get recent interactions"""
        return list(self.recent_interactions)[-limit:]
    
    def get_last_sensor_data(self, sensor_name: str) -> Optional[SensorData]:
        """Get most recent sensor data"""
        return self.sensor_cache.get(sensor_name)
    
    def cache_reasoning_result(self, key: str, result: Any, ttl_seconds: int = 300):
        """Cache reasoning result with TTL"""
        self.reasoning_cache[key] = {
            "result": result,
            "timestamp": datetime.now(),
            "ttl": ttl_seconds
        }
    
    def get_cached_reasoning(self, key: str) -> Optional[Any]:
        """Get cached reasoning result if still valid"""
        if key not in self.reasoning_cache:
            self.cache_misses += 1
            return None
        
        cached = self.reasoning_cache[key]
        age = (datetime.now() - cached["timestamp"]).total_seconds()
        
        if age > cached["ttl"]:
            del self.reasoning_cache[key]
            self.cache_misses += 1
            return None
        
        self.cache_hits += 1
        return cached["result"]
    
    def set_context(self, key: str, value: Any):
        """Set current context state"""
        self.context_state[key] = {
            "value": value,
            "updated_at": datetime.now()
        }
    
    def get_context(self, key: str) -> Optional[Any]:
        """Get current context state"""
        if key in self.context_state:
            return self.context_state[key]["value"]
        return None
    
    def update_context(self, updates: Dict[str, Any]):
        """Update multiple context values"""
        for key, value in updates.items():
            self.set_context(key, value)
    
    def get_full_context(self) -> Dict[str, Any]:
        """Get entire context state"""
        return {k: v["value"] for k, v in self.context_state.items()}
    
    def _purge_old_data(self):
        """Remove data older than retention period"""
        cutoff_time = datetime.now() - timedelta(seconds=self.retention_seconds)
        
        # Purge old sensor data
        expired_sensors = [
            name for name, data in self.sensor_cache.items()
            if data.timestamp < cutoff_time
        ]
        for sensor in expired_sensors:
            del self.sensor_cache[sensor]
        
        # Purge old reasoning cache
        expired_keys = [
            key for key, cached in self.reasoning_cache.items()
            if (datetime.now() - cached["timestamp"]).total_seconds() > cached["ttl"]
        ]
        for key in expired_keys:
            del self.reasoning_cache[key]
    
    def clear(self):
        """Clear all working memory"""
        self.recent_interactions.clear()
        self.sensor_cache.clear()
        self.reasoning_cache.clear()
        self.context_state.clear()
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get working memory performance statistics"""
        total = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total * 100) if total > 0 else 0
        
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate_percent": hit_rate,
            "interactions_stored": len(self.recent_interactions),
            "sensor_entries": len(self.sensor_cache),
            "reasoning_cache_size": len(self.reasoning_cache),
            "context_entries": len(self.context_state)
        }
    
    def optimize_memory(self):
        """Optimize memory usage"""
        # Remove least important cached reasoning
        if len(self.reasoning_cache) > self.max_entries / 2:
            # Keep only most recent
            sorted_cache = sorted(
                self.reasoning_cache.items(),
                key=lambda x: x[1]["timestamp"]
            )
            keys_to_remove = len(sorted_cache) - int(self.max_entries / 4)
            for key, _ in sorted_cache[:keys_to_remove]:
                del self.reasoning_cache[key]
