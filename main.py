from voice_input import get_voice_input
from llama_client import get_llama_response
from text_to_speech import speak

def main():
    """
    Main controller - Glues all modules together
    Flow: Listen → Send to LLaMA → Speak response
    """
    print("=" * 50)
    print("🎤 Voice LLaMA Chatbot Started")
    print("=" * 50)
    print("💡 Say 'exit' to quit\n")
    
    while True:
        # Step 1: Get voice input
        user_text = get_voice_input()
        
        # Check if user wants to exit
        if user_text.lower() == "exit":
            print("\n👋 Goodbye!")
            speak("Goodbye!")
            break
        
        # Skip if no text was recognized
        if not user_text:
            print("⚠️ Please try again\n")
            continue
        
        # Step 2: Send to LLaMA
        llama_response = get_llama_response(user_text)
        
        # Skip if no response
        if not llama_response:
            print("⚠️ No response from LLaMA\n")
            continue
        
        # Step 3: Print response
        print("\n" + "=" * 50)
        print(f"📄 Response:\n{llama_response}")
        print("=" * 50 + "\n")
        
        # Step 4: Speak response
        speak(llama_response)
        
        print("-" * 50 + "\n")

if __name__ == "__main__":
    main()
