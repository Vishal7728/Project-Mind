#!/usr/bin/env python3
"""
Project Mind - Living AI Companion
Main Application Entry Point
"""

import os
import sys

# Add the app/src directory to the path to allow relative imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy_main import ProjectMindApp

if __name__ == '__main__':
    ProjectMindApp().run()