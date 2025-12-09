#!/bin/bash
# Build script for Project Mind APK

echo "Building Project Mind APK..."
cd ..

# Validate build environment
python scripts/validate_build.py

# Build APK using Buildozer
buildozer -v android release

echo "Build completed!"