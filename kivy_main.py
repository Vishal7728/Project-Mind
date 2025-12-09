#!/usr/bin/env python

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import ProjectMind
from src.types import PhoneSpecifications, EmotionalState

Window.size = (400, 800)


class ProjectMindApp(App):
    
    def build(self):
        self.title = "Project Mind - Living AI"
        
        try:
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
            
            self.project_mind = ProjectMind(phone_specs)
            self.project_mind.initialize()
            
        except Exception as e:
            print(f"Error initializing ProjectMind: {e}")
            self.project_mind = None
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title_label = Label(
            text="Project Mind - Living AI",
            size_hint_y=0.1,
            font_size='24sp',
            bold=True
        )
        main_layout.add_widget(title_label)
        
        face_container = BoxLayout(size_hint_y=0.4, padding=5)
        face_placeholder = Label(text="[AI Face Display Area]", color=(0.2, 0.6, 0.8, 1))
        face_container.add_widget(face_placeholder)
        main_layout.add_widget(face_container)
        
        scroll_view = ScrollView(size_hint_y=0.35)
        scroll_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        
        self.status_label = Label(
            text=self.get_status_text(),
            size_hint_y=None,
            height=100,
            markup=True
        )
        scroll_layout.add_widget(self.status_label)
        
        scroll_view.add_widget(scroll_layout)
        main_layout.add_widget(scroll_view)
        
        controls_layout = GridLayout(cols=2, spacing=5, size_hint_y=0.15)
        
        name_btn = Button(text="Set Name")
        name_btn.bind(on_press=self.show_naming_dialog)
        controls_layout.add_widget(name_btn)
        
        persona_btn = Button(text="Custom Persona")
        persona_btn.bind(on_press=self.show_persona_dialog)
        controls_layout.add_widget(persona_btn)
        
        voice_btn = Button(text="Voice Settings")
        voice_btn.bind(on_press=self.show_voice_dialog)
        controls_layout.add_widget(voice_btn)
        
        emotion_btn = Button(text="Show Emotion")
        emotion_btn.bind(on_press=self.show_emotion_dialog)
        controls_layout.add_widget(emotion_btn)
        
        main_layout.add_widget(controls_layout)
        
        Clock.schedule_interval(self.update_status, 2.0)
        
        return main_layout
    
    def get_status_text(self):
        if not self.project_mind:
            return "Initializing..."
        
        try:
            status = self.project_mind.get_status()
            emotion = status.get('emotion', 'neutral') if status else 'neutral'
            age = status.get('age_days', 0) if status else 0
            trust = status.get('trust_level', 0.5) if status else 0.5
            return f"[b]AI Status:[/b]\nAge: {age} days\nEmotion: {emotion}\nTrust: {trust:.2f}"
        except Exception as e:
            return f"Status: Ready"
    
    def update_status(self, dt):
        self.status_label.text = self.get_status_text()
    
    def show_naming_dialog(self, instance):
        if not self.project_mind:
            return
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        try:
            ai_name = self.project_mind.heart.profile.get('ai_name', 'Mind') if self.project_mind.heart else 'Mind'
            user_name = self.project_mind.heart.profile.get('user_name', '') if self.project_mind.heart else ''
        except:
            ai_name = 'Mind'
            user_name = ''
        
        ai_name_input = TextInput(
            text=ai_name,
            multiline=False,
            hint_text="AI Name"
        )
        content.add_widget(Label(text="AI Name:"))
        content.add_widget(ai_name_input)
        
        user_name_input = TextInput(
            text=user_name,
            multiline=False,
            hint_text="Your Name"
        )
        content.add_widget(Label(text="Your Name:"))
        content.add_widget(user_name_input)
        
        button_layout = BoxLayout(size_hint_y=0.2, spacing=5)
        
        def save_names(btn):
            try:
                if self.project_mind.heart:
                    if ai_name_input.text:
                        self.project_mind.heart.profile['ai_name'] = ai_name_input.text
                    if user_name_input.text:
                        self.project_mind.heart.profile['user_name'] = user_name_input.text
                    self.project_mind.heart.save()
            except Exception as e:
                print(f"Error saving names: {e}")
            finally:
                popup.dismiss()
        
        save_btn = Button(text="Save")
        save_btn.bind(on_press=save_names)
        button_layout.add_widget(save_btn)
        
        close_btn = Button(text="Close")
        close_btn.bind(on_press=lambda x: popup.dismiss())
        button_layout.add_widget(close_btn)
        
        content.add_widget(button_layout)
        
        popup = Popup(
            title="Naming Settings",
            content=content,
            size_hint=(0.9, 0.6)
        )
        popup.open()
    
    def show_persona_dialog(self, instance):
        if not self.project_mind:
            return
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        content.add_widget(Label(text="Persona Customization", size_hint_y=0.1, bold=True))
        
        scroll = ScrollView()
        scroll_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        
        archetype_label = Label(text="Select Archetype:", size_hint_y=None, height=40)
        scroll_layout.add_widget(archetype_label)
        
        archetypes = ["WISE_MENTOR", "SUPPORTIVE_FRIEND", "PLAYFUL_COMPANION", 
                      "PROFESSIONAL_ADVISOR", "ARTISTIC_CREATIVE", "LOGICAL_ANALYST",
                      "ADVENTUROUS_EXPLORER", "NURTURING_CAREGIVER", "MYSTICAL_GUIDE"]
        
        for archetype in archetypes:
            btn = Button(text=archetype.replace('_', ' '), size_hint_y=None, height=40)
            btn.archetype_val = archetype
            btn.bind(on_press=self.create_persona_callback(archetype))
            scroll_layout.add_widget(btn)
        
        scroll.add_widget(scroll_layout)
        content.add_widget(scroll)
        
        button_layout = BoxLayout(size_hint_y=0.15, spacing=5)
        close_btn = Button(text="Close")
        close_btn.bind(on_press=lambda x: popup.dismiss())
        button_layout.add_widget(close_btn)
        content.add_widget(button_layout)
        
        popup = Popup(
            title="Custom Persona",
            content=content,
            size_hint=(0.9, 0.7)
        )
        popup.open()
    
    def create_persona_callback(self, archetype):
        def callback(instance):
            self.set_persona_archetype(archetype)
        return callback
    
    def set_persona_archetype(self, archetype):
        if not self.project_mind:
            return
        
        try:
            from src.types import PersonaProfile
            profile = PersonaProfile(archetype=archetype)
            self.project_mind.persona_engine.apply_persona(profile)
        except Exception as e:
            print(f"Error setting persona: {e}")
    
    def show_voice_dialog(self, instance):
        if not self.project_mind:
            return
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        content.add_widget(Label(text="Voice Configuration", size_hint_y=0.1, bold=True))
        
        try:
            voice_stage = self.project_mind.heart.profile.get('voice_stage', 1) if self.project_mind.heart else 1
            info_text = f"Voice Stage: {voice_stage}/5\nEvolving with interactions..."
        except:
            info_text = "Voice Stage: 1/5\nEvolving with interactions..."
        
        content.add_widget(Label(text=info_text, size_hint_y=0.3))
        
        button_layout = BoxLayout(size_hint_y=0.2, spacing=5)
        test_btn = Button(text="Test Voice")
        test_btn.bind(on_press=self.test_voice)
        button_layout.add_widget(test_btn)
        
        close_btn = Button(text="Close")
        close_btn.bind(on_press=lambda x: popup.dismiss())
        button_layout.add_widget(close_btn)
        content.add_widget(button_layout)
        
        popup = Popup(
            title="Voice Settings",
            content=content,
            size_hint=(0.9, 0.5)
        )
        popup.open()
    
    def test_voice(self, instance):
        if not self.project_mind:
            return
        
        try:
            self.project_mind.voice_evolution_engine.synthesize_speech(
                "Hello! I am Project Mind, your personal AI companion!"
            )
        except Exception as e:
            print(f"Error in voice synthesis: {e}")
    
    def show_emotion_dialog(self, instance):
        if not self.project_mind:
            return
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        content.add_widget(Label(text="Select Emotion:", size_hint_y=0.1, bold=True))
        
        emotions = ["HAPPY", "EXCITED", "CALM", "CONCERNED", "CURIOUS", "PROTECTIVE"]
        button_layout = GridLayout(cols=2, spacing=5, size_hint_y=0.6)
        
        for emotion in emotions:
            btn = Button(text=emotion)
            btn.emotion_val = emotion
            btn.bind(on_press=self.create_emotion_callback(emotion))
            button_layout.add_widget(btn)
        
        content.add_widget(button_layout)
        
        close_btn = Button(text="Close", size_hint_y=0.2)
        close_btn.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        
        popup = Popup(
            title="Emotion Expression",
            content=content,
            size_hint=(0.9, 0.6)
        )
        popup.open()
    
    def create_emotion_callback(self, emotion_name):
        def callback(instance):
            self.show_emotion(emotion_name)
        return callback
    
    def show_emotion(self, emotion_name):
        if not self.project_mind:
            return
        
        try:
            if hasattr(EmotionalState, emotion_name):
                emotion = getattr(EmotionalState, emotion_name)
                self.project_mind.emotion_engine.update_emotion(emotion)
                self.project_mind.gui_engine.update_facial_expression(emotion)
        except Exception as e:
            print(f"Error updating emotion: {e}")


if __name__ == '__main__':
    ProjectMindApp().run()
