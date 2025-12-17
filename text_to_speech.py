import pyttsx3
import threading
import time

# Global flag to stop speech
_stop_speech = False
_speech_thread = None
_speech_engine = None

def stop_speech():
    """Stop current speech immediately"""
    global _stop_speech, _speech_engine
    _stop_speech = True
    
    # Stop the engine if it exists
    if _speech_engine:
        try:
            _speech_engine.stop()
        except:
            pass

def speak(text):
    """
    Converts text to speech using pyttsx3 (runs in background thread)
    Args: text (string) - Text to be spoken
    """
    global _stop_speech, _speech_thread
    
    if not text:
        return
    
    _stop_speech = False
    
    # Run speech in background thread
    _speech_thread = threading.Thread(target=_speak_sync, args=(text,), daemon=True)
    _speech_thread.start()

def _speak_sync(text):
    """Internal function to actually speak (blocking)"""
    global _stop_speech, _speech_engine
    
    try:
        # Initialize text-to-speech engine
        _speech_engine = pyttsx3.init()
        
        # Set speed
        _speech_engine.setProperty('rate', 150)
        
        # Limit response length to avoid too long speech
        max_length = 500
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        # Check if already stopped
        if _stop_speech:
            return
        
        # Break text into chunks for faster stop response
        sentences = text.split('. ')
        
        for i, sentence in enumerate(sentences):
            # Check if stop was requested
            if _stop_speech:
                try:
                    _speech_engine.stop()
                except:
                    pass
                break
            
            # Add period back if not last sentence
            if i < len(sentences) - 1:
                sentence += '. '
            
            try:
                _speech_engine.say(sentence)
                _speech_engine.runAndWait()
            except:
                pass
        
        _speech_engine = None
        
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        _speech_engine = None


