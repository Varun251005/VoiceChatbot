import speech_recognition as sr

def get_voice_input():
    """
    Records audio from microphone and converts to text using Google Speech Recognition
    Returns: Recognized text as string
    """
    recognizer = sr.Recognizer()
    
    # Use microphone as audio source
    with sr.Microphone() as source:
        try:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Record audio
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=20)
            
            # Use Google Speech Recognition (built-in, no FFmpeg needed)
            text = recognizer.recognize_google(audio)
            
            return text
            
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"❌ Error: {e}")
            return ""
