#!/bin/bash
# Environment setup script for Project Mind

echo "Setting up environment for Project Mind..."

# Export environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export PROJECT_MIND_HOME="$(pwd)"

echo "Environment setup completed!"
echo "PYTHONPATH: $PYTHONPATH"
echo "PROJECT_MIND_HOME: $PROJECT_MIND_HOME"