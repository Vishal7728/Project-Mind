#!/usr/bin/env python3
"""
Test script to verify the Project Mind app structure and imports
"""

import sys
import os

# Add the app source directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app', 'src'))

def test_imports():
    """Test importing key modules"""
    try:
        # Test importing the main app module
        from kivy_main import ProjectMindApp
        print("✓ Successfully imported kivy_main")
        
        # Test importing the main class
        from main import ProjectMind
        print("✓ Successfully imported ProjectMind")
        
        # Test importing types
        from types import PhoneSpecifications
        print("✓ Successfully imported types")
        
        # Test importing core modules
        from core.naming_engine import NamingEngine
        print("✓ Successfully imported naming_engine")
        
        from personality.emotion_engine import EmotionEngine
        print("✓ Successfully imported emotion_engine")
        
        from memory.heart import Heart
        print("✓ Successfully imported heart")
        
        from presentation.gui_engine import GuiEngine
        print("✓ Successfully imported gui_engine")
        
        print("\n🎉 All imports successful! Project structure is correct.")
        return True
        
    except Exception as e:
        print(f"✗ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_project_mind_initialization():
    """Test initializing the ProjectMind class"""
    try:
        from main import ProjectMind
        from types import PhoneSpecifications
        
        # Create phone specifications
        phone_specs = PhoneSpecifications(
            ram_gb=4,
            cpu_cores=8,
            screen_width_px=400,
            screen_height_px=800,
            has_camera=True,
            has_microphone=True,
            has_speakers=True,
            gpu_capable=True
        )
        
        # Initialize ProjectMind
        project_mind = ProjectMind(phone_specs)
        print("✓ Successfully initialized ProjectMind")
        
        # Test accessing core components
        print(f"  - Heart initialized: {project_mind.heart is not None}")
        print(f"  - Emotion Engine initialized: {project_mind.emotion_engine is not None}")
        print(f"  - Naming Engine initialized: {project_mind.naming_engine is not None}")
        
        return True
        
    except Exception as e:
        print(f"✗ Initialization error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Project Mind app structure...\n")
    
    if test_imports():
        print("\nTesting ProjectMind initialization...")
        if test_project_mind_initialization():
            print("\n🎉 All tests passed! Project is ready for build.")
        else:
            print("\n❌ Initialization tests failed.")
    else:
        print("\n❌ Import tests failed.")