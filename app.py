from flask import Flask, render_template, request, jsonify
from voice_input import get_voice_input
from llama_client import get_llama_response, stop_generation
from text_to_speech import speak, stop_speech
import threading

app = Flask(__name__)

# Global state
current_task = None
should_stop = False

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/listen', methods=['POST'])
def listen():
    """Record voice and convert to text"""
    global should_stop
    should_stop = False
    
    try:
        text = get_voice_input()
        
        if not text:
            return jsonify({'success': False, 'error': 'No audio detected'})
        
        return jsonify({'success': True, 'text': text})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/generate', methods=['POST'])
def generate():
    """Send text to LLaMA and get response"""
    global should_stop
    should_stop = False
    
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'})
        
        response = get_llama_response(text)
        
        if should_stop:
            return jsonify({'success': False, 'error': 'Skipped'})
        
        if not response:
            return jsonify({'success': False, 'error': 'No response from LLaMA'})
        
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/speak', methods=['POST'])
def speak_response():
    """Convert response to speech"""
    global should_stop
    
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'})
        
        speak(text)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/stop', methods=['POST'])
def stop():
    """Stop current operation"""
    global should_stop
    should_stop = True
    stop_generation()
    stop_speech()  # Stop the speech immediately
    
    return jsonify({'success': True})

if __name__ == '__main__':
    print("=" * 50)
    print("🎤 VRNX CHATBOT - Web Server Started")
    print("=" * 50)
    print("🌐 Open your browser: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, port=5000, use_reloader=False)
