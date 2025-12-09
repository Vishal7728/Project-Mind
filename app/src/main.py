#!/usr/bin/env python3
"""
Project Mind - Living AI Companion
Main Application Entry Point
"""

import os
import sys

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy_main import ProjectMindApp

if __name__ == '__main__':
    ProjectMindApp().run()