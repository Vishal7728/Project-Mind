"""
Project Mind - __init__.py
Package initialization
"""

__version__ = "1.0.0"
__name__ = "Project Mind"
__description__ = "A living, emotionally intelligent AI for phones"
__author__ = "Project Mind Team"

from src.main import ProjectMind
from src.types import (
    PhoneSpecifications, 
    PermissionType, 
    EmotionalState,
    ContextProfile,
    PhoneSpecLevel
)

__all__ = [
    "ProjectMind",
    "PhoneSpecifications",
    "PermissionType",
    "EmotionalState",
    "ContextProfile",
    "PhoneSpecLevel"
]
