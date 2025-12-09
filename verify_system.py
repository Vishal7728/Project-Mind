import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def verify_imports():
    try:
        from src.main import ProjectMind
        from src.types import PhoneSpecifications, PersonaProfile, NameProfile
        from src.presentation.persona_engine import PersonaEngine
        from src.presentation.gui_engine import GuiEngine
        from src.presentation.voice_evolution_engine import VoiceEvolutionEngine
        from src.personality.emotion_engine import PersonalityEngine
        from src.core.naming_engine import NamingEngine
        from src.memory.heart import Heart
        return True, "All imports successful"
    except Exception as e:
        return False, f"Import error: {str(e)}"


def verify_persona_system():
    try:
        from src.presentation.persona_engine import PersonaEngine
        engine = PersonaEngine()
        
        questionnaire = engine.get_persona_questionnaire()
        if len(questionnaire) != 11:
            return False, f"Questionnaire has {len(questionnaire)} questions, expected 11"
        
        modifiers = engine.get_personality_modifiers()
        if not isinstance(modifiers, dict):
            return False, "Modifiers not returned as dict"
        
        return True, "Persona system verified"
    except Exception as e:
        return False, f"Persona error: {str(e)}"


def verify_naming_system():
    try:
        from src.core.naming_engine import NamingEngine
        engine = NamingEngine()
        
        engine.set_ai_name("TestMind")
        engine.set_user_name("TestUser")
        
        greeting = engine.get_personalized_greeting()
        if not greeting:
            return False, "No greeting generated"
        
        return True, "Naming system verified"
    except Exception as e:
        return False, f"Naming error: {str(e)}"


def verify_type_definitions():
    try:
        from src.types import (
            PersonaProfile, PersonaArchetype, PersonaFaceProfile,
            PersonaBehaviorProfile, PersonaVoiceProfile,
            NameProfile, NamingStatus, NameChangeInitiator
        )
        return True, "All types present"
    except ImportError as e:
        return False, f"Missing type: {str(e)}"


def verify_presentation_integration():
    try:
        from src.presentation.presentation_manager import PresentationManager
        from src.presentation.persona_engine import PersonaEngine
        
        pm = PresentationManager()
        pe = PersonaEngine()
        pm.set_persona(pe)
        
        status = pm.get_persona_status()
        if status is None:
            return False, "Persona status not returned"
        
        return True, "Presentation integration verified"
    except Exception as e:
        return False, f"Integration error: {str(e)}"


def verify_memory_integration():
    try:
        from src.memory.heart import Heart
        from src.types import PersonaProfile
        
        heart = Heart("test_heart.json")
        if not hasattr(heart, 'persona_profile'):
            return False, "Heart missing persona_profile attribute"
        
        return True, "Memory integration verified"
    except Exception as e:
        return False, f"Memory error: {str(e)}"


def verify_files():
    required_files = [
        "src/main.py",
        "src/types.py",
        "src/presentation/persona_engine.py",
        "src/presentation/gui_engine.py",
        "src/presentation/voice_evolution_engine.py",
        "src/presentation/presentation_manager.py",
        "src/core/naming_engine.py",
        "src/personality/emotion_engine.py",
        "src/memory/heart.py",
        "buildozer.spec",
        "kivy_main.py",
        "build_apk.py",
        "README.md"
    ]
    
    missing = [f for f in required_files if not os.path.exists(f)]
    
    if missing:
        return False, f"Missing files: {', '.join(missing)}"
    
    return True, f"All {len(required_files)} required files present"


def main():
    print("""
    ╔════════════════════════════════════════╗
    ║  Project Mind - System Verification    ║
    ║  Full Feature Completion Check         ║
    ╚════════════════════════════════════════╝
    """)
    
    tests = [
        ("File Structure", verify_files),
        ("Type Definitions", verify_type_definitions),
        ("Import System", verify_imports),
        ("Persona System", verify_persona_system),
        ("Naming System", verify_naming_system),
        ("Memory Integration", verify_memory_integration),
        ("Presentation Integration", verify_presentation_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        success, message = test_func()
        status = "✓" if success else "✗"
        print(f"[{status}] {test_name}: {message}")
        results.append(success)
    
    print("\n" + "="*50)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if all(results):
        print("\n✓ All systems verified successfully!")
        print("Project Mind is ready for deployment.")
        return 0
    else:
        print("\n✗ Some systems need attention.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
