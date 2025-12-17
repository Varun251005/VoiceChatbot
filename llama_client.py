import requests
import json

# Global flag to stop generation
_stop_generation = False

def stop_generation():
    """Set flag to stop generation"""
    global _stop_generation
    _stop_generation = True

def get_llama_response(user_text):
    """
    Sends user text to local Ollama LLaMA API and returns response
    Returns: Response text from LLaMA
    """
    global _stop_generation
    _stop_generation = False
    
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": "llama3.2",
        "prompt": user_text,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=300)
        
        if _stop_generation:
            return ""
        
        if response.status_code == 200:
            result = response.json()
            llama_text = result.get("response", "")
            return llama_text
        else:
            return ""
            
    except requests.exceptions.ConnectionError:
        return ""
    except Exception as e:
        return ""
