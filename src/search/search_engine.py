"""
Search Engine Connector Module
Internal memory search + user-approved internet search
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple
from src.types import SearchQuery


class SearchEngine:
    """
    Manages search functionality: internal memory search and internet search.
    Always confirms with user before performing internet search.
    """
    
    def __init__(self, internet_search_enabled: bool = False):
        self.internet_search_enabled = internet_search_enabled
        self.search_history: List[SearchQuery] = []
        
        # Simulated internet search (in production, would use API)
        self.mock_search_results = self._init_mock_results()
    
    def _init_mock_results(self) -> Dict[str, List[str]]:
        """Initialize mock search results"""
        return {
            "python tutorial": [
                "Python is a high-level programming language...",
                "Learn Python basics: variables, functions, classes...",
                "Python libraries: numpy, pandas, scikit-learn...",
            ],
            "weather today": [
                "Today's weather forecast: Partly cloudy, 72°F...",
                "UV index: Moderate, Humidity: 65%...",
            ],
            "meditation techniques": [
                "Deep breathing meditation for stress relief...",
                "Mindfulness meditation for better focus...",
                "Body scan meditation for relaxation...",
            ],
        }
    
    def search_internal_memory(self, query: str, memory_entries: List[any]) -> List[any]:
        """Search internal long-term memory"""
        start_time = datetime.now()
        
        results = []
        query_lower = query.lower()
        
        for entry in memory_entries:
            # Search in content and tags
            if (query_lower in entry.content.lower() or
                any(query_lower in tag.lower() for tag in getattr(entry, 'tags', []))):
                results.append(entry)
        
        # Sort by importance and recency
        results.sort(
            key=lambda e: (getattr(e, 'importance_score', 0), getattr(e, 'timestamp', datetime.now())),
            reverse=True
        )
        
        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        
        search_query = SearchQuery(
            query=query,
            timestamp=datetime.now(),
            search_type="internal",
            results_count=len(results),
            execution_time_ms=execution_time,
            cached=False
        )
        self.search_history.append(search_query)
        
        return results[:10]  # Limit to top 10
    
    def search_internet(self, query: str, user_approved: bool = False) -> Optional[List[str]]:
        """Search internet (requires user approval)"""
        if not user_approved:
            return None
        
        if not self.internet_search_enabled:
            return None
        
        start_time = datetime.now()
        
        # In production, would use real API (Google, Bing, etc.)
        # For now, return mock results
        results = self._get_mock_search_results(query)
        
        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        
        search_query = SearchQuery(
            query=query,
            timestamp=datetime.now(),
            search_type="internet",
            results_count=len(results),
            execution_time_ms=execution_time,
            cached=False
        )
        self.search_history.append(search_query)
        
        return results
    
    def _get_mock_search_results(self, query: str) -> List[str]:
        """Get mock internet search results"""
        query_lower = query.lower()
        
        # Simple keyword matching for demo
        for keyword, results in self.mock_search_results.items():
            if keyword in query_lower or query_lower in keyword:
                return results
        
        # Default result
        return [f"Search results for: {query}"]
    
    def search_combined(self, query: str, memory_entries: List[any],
                       search_internet: bool = False,
                       user_approved: bool = False) -> Dict[str, any]:
        """Perform combined search (internal + internet)"""
        results = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "internal_results": [],
            "internet_results": None,
            "combined_insights": ""
        }
        
        # Always search internal first
        internal_results = self.search_internal_memory(query, memory_entries)
        results["internal_results"] = [
            {
                "type": "memory_entry",
                "content": entry.content[:200],
                "importance": getattr(entry, 'importance_score', 0),
                "timestamp": entry.timestamp.isoformat()
            }
            for entry in internal_results
        ]
        
        # Search internet if requested and approved
        if search_internet and user_approved:
            internet_results = self.search_internet(query, user_approved=True)
            if internet_results:
                results["internet_results"] = internet_results[:3]  # Top 3
        
        # Generate combined insights
        if results["internal_results"] and results["internet_results"]:
            results["combined_insights"] = (
                f"Found {len(results['internal_results'])} internal memories and "
                f"{len(results['internet_results'])} internet results about '{query}'."
            )
        elif results["internal_results"]:
            results["combined_insights"] = (
                f"Found {len(results['internal_results'])} relevant memories about '{query}'."
            )
        elif results["internet_results"]:
            results["combined_insights"] = (
                f"Found {len(results['internet_results'])} results about '{query}' online."
            )
        else:
            results["combined_insights"] = f"No results found for '{query}'."
        
        return results
    
    def request_internet_search_permission(self, query: str) -> Dict[str, any]:
        """Request user permission for internet search"""
        return {
            "requires_approval": True,
            "message": f"May I search the internet for '{query}'? This will help me give you better information.",
            "query": query,
            "action": "request_user_approval"
        }
    
    def get_search_history(self, limit: int = 20) -> List[Dict[str, any]]:
        """Get search history"""
        recent = self.search_history[-limit:]
        return [
            {
                "query": sq.query,
                "type": sq.search_type,
                "results": sq.results_count,
                "time_ms": sq.execution_time_ms,
                "timestamp": sq.timestamp.isoformat()
            }
            for sq in recent
        ]
    
    def get_search_stats(self) -> Dict[str, any]:
        """Get search statistics"""
        internal_searches = [s for s in self.search_history if s.search_type == "internal"]
        internet_searches = [s for s in self.search_history if s.search_type == "internet"]
        
        avg_internal_time = (
            sum(s.execution_time_ms for s in internal_searches) / len(internal_searches)
            if internal_searches else 0
        )
        
        avg_internet_time = (
            sum(s.execution_time_ms for s in internet_searches) / len(internet_searches)
            if internet_searches else 0
        )
        
        return {
            "total_searches": len(self.search_history),
            "internal_searches": len(internal_searches),
            "internet_searches": len(internet_searches),
            "avg_internal_search_ms": avg_internal_time,
            "avg_internet_search_ms": avg_internet_time,
            "internet_search_enabled": self.internet_search_enabled
        }
