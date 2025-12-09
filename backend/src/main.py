#!/usr/bin/env python3
"""
Project Mind Backend Server
"""

from flask import Flask, jsonify, request
import os
import sys

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

@app.route('/api/v1/status')
def status():
    """Return the current status of the AI system."""
    return jsonify({
        "status": "running",
        "version": "1.0.0",
        "uptime": "0 days, 0 hours, 0 minutes"
    })

@app.route('/api/v1/chat', methods=['POST'])
def chat():
    """Process a chat message from the user."""
    data = request.get_json()
    
    # In a real implementation, this would connect to the AI engine
    response = {
        "response": f"I received your message: {data.get('message', '')}",
        "emotion": "curious",
        "timestamp": "2025-12-09T21:00:00Z"
    }
    
    return jsonify(response)

@app.route('/api/v1/memory')
def memory():
    """Return the AI's memory state."""
    return jsonify({
        "short_term": {},
        "long_term": {}
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)