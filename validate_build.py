#!/usr/bin/env python3
"""
Comprehensive build validation script
Runs before APK build to catch potential errors early
"""

import os
import sys
import ast
import json
from pathlib import Path

class BuildValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        
    def validate_all(self):
        """Run all validation checks"""
        print("="*80)
        print("BUILD VALIDATION REPORT")
        print("="*80)
        
        self.check_python_files()
        self.check_buildozer_spec()
        self.check_data_files()
        self.check_imports()
        self.check_android_specific()
        
        self.print_report()
        return len(self.errors) == 0
    
    def check_python_files(self):
        """Validate all Python files"""
        print("\n1. Validating Python files...")
        
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.github', 'bin', 'data']]
            
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            code = f.read()
                        ast.parse(code)
                        self.info.append(f"Python: {filepath} OK")
                    except SyntaxError as e:
                        self.errors.append(f"Syntax error in {filepath}: {e.msg}")
                    except Exception as e:
                        self.errors.append(f"Error reading {filepath}: {str(e)}")
    
    def check_buildozer_spec(self):
        """Validate buildozer.spec configuration"""
        print("\n2. Validating buildozer.spec...")
        
        if not os.path.exists('buildozer.spec'):
            self.errors.append("buildozer.spec not found!")
            return
        
        with open('buildozer.spec', 'r') as f:
            spec_content = f.read()
        
        required_keys = [
            'title',
            'package.name',
            'package.domain',
            'version',
            'android.api',
            'android.minapi',
            'android.archs',
            'requirements',
        ]
        
        for key in required_keys:
            if key in spec_content:
                self.info.append(f"Spec: {key} found")
            else:
                self.errors.append(f"Missing in buildozer.spec: {key}")
        
        # Check for problematic settings
        if 'android.logcat_filters' in spec_content:
            self.warnings.append("Found android.logcat_filters - consider removing for build stability")
        
        # Validate API levels
        import re
        api_match = re.search(r'android.api = (\d+)', spec_content)
        minapi_match = re.search(r'android.minapi = (\d+)', spec_content)
        
        if api_match and minapi_match:
            api = int(api_match.group(1))
            minapi = int(minapi_match.group(1))
            if minapi > api:
                self.errors.append("minapi cannot be greater than api")
            else:
                self.info.append(f"API levels OK: api={api}, minapi={minapi}")
    
    def check_data_files(self):
        """Check required data files"""
        print("\n3. Checking data files...")
        
        required_files = [
            'data/mind_heart.json',
            'test_heart.json',
        ]
        
        for filepath in required_files:
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                self.info.append(f"Data: {filepath} ({size} bytes)")
                
                # Try to parse JSON
                try:
                    with open(filepath, 'r') as f:
                        json.load(f)
                    self.info.append(f"JSON: {filepath} is valid")
                except json.JSONDecodeError as e:
                    self.errors.append(f"Invalid JSON in {filepath}: {e}")
            else:
                self.warnings.append(f"Data file not found: {filepath}")
    
    def check_imports(self):
        """Check if all imports are available"""
        print("\n4. Checking critical imports...")
        
        critical_imports = [
            'src.main',
            'src.types',
            'src.memory.heart',
            'src.personality.emotion_engine',
            'src.presentation.gui_engine',
            'src.presentation.persona_engine',
            'src.presentation.voice_evolution_engine',
        ]
        
        for module in critical_imports:
            try:
                __import__(module)
                self.info.append(f"Import: {module} OK")
            except ImportError as e:
                self.errors.append(f"Cannot import {module}: {e}")
            except Exception as e:
                self.errors.append(f"Error importing {module}: {str(e)}")
    
    def check_android_specific(self):
        """Check Android-specific issues"""
        print("\n5. Checking Android configuration...")
        
        with open('buildozer.spec', 'r') as f:
            spec = f.read()
        
        # Check architecture support
        if 'arm64-v8a' in spec or 'armeabi-v7a' in spec:
            self.info.append("Android: 32/64-bit architecture support configured")
        else:
            self.warnings.append("Only one architecture configured - consider adding both 32 and 64-bit")
        
        # Check permissions
        if 'permissions' in spec:
            import re
            perms = re.search(r'permissions = (.+)', spec)
            if perms:
                perm_list = perms.group(1).split(',')
                self.info.append(f"Android: {len(perm_list)} permissions configured")
        
        # Check entry point
        if 'org.renpy.android.PythonActivity' in spec:
            self.info.append("Android: PythonActivity entry point configured")
        else:
            self.warnings.append("Unknown Android entry point")
    
    def print_report(self):
        """Print validation report"""
        print("\n" + "="*80)
        print("VALIDATION REPORT SUMMARY")
        print("="*80)
        
        if self.info:
            print(f"\nInfo ({len(self.info)} items):")
            for msg in self.info[-10:]:  # Show last 10
                print(f"  [OK] {msg}")
            if len(self.info) > 10:
                print(f"  ... and {len(self.info)-10} more")
        
        if self.warnings:
            print(f"\nWarnings ({len(self.warnings)} items):")
            for msg in self.warnings:
                print(f"  [WARN] {msg}")
        
        if self.errors:
            print(f"\nErrors ({len(self.errors)} items):")
            for msg in self.errors:
                print(f"  [ERROR] {msg}")
        
        print("\n" + "="*80)
        if not self.errors:
            print("RESULT: VALIDATION PASSED - Ready for APK build")
            print("="*80)
            return 0
        else:
            print(f"RESULT: VALIDATION FAILED - {len(self.errors)} error(s) to fix")
            print("="*80)
            return 1

if __name__ == '__main__':
    validator = BuildValidator()
    sys.exit(0 if validator.validate_all() else 1)
