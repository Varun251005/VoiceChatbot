from voice_input import get_voice_input
from llama_client import get_llama_response
from text_to_speech import speak
import os


def main():
    """Main controller - accepts text or voice input, replies in text and speech."""
    print("=" * 50)
    print("🎤 Voice LLaMA Chatbot Started")
    print("=" * 50)
    print("💡 Type a message or press Enter to speak. Say 'exit' to quit.\n")

    while True:
        # Prompt user: typed input or voice
        try:
            prompt = input("Type message or press Enter to speak (or 'exit'): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            speak("Goodbye!")
            break

        # Exit immediately if typed 'exit'
        if prompt.lower() == "exit":
            print("\n👋 Goodbye!")
            speak("Goodbye!")
            break

        # Use typed input if provided, otherwise use voice
        if prompt:
            user_text = prompt
            print(f"📝 You typed: {user_text}")
        else:
            print("\n🎤 Listening... Speak now!")
            user_text = get_voice_input()
            if user_text:
                print(f"📝 You said: {user_text}")

        # Check if we got any input
        if not user_text:
            print("⚠️ No input detected. Please try again\n")
            continue

        # Send to LLaMA (provide fallback API key from env if present)
        fallback_key = os.getenv("FALLBACK_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        llama_response = get_llama_response(user_text, fallback_api_key=fallback_key)

        if not llama_response:
            print("⚠️ No response from LLaMA\n")
            continue

        # Print and speak response
        print("\n" + "=" * 50)
        print(f"📄 Response:\n{llama_response}")
        print("=" * 50 + "\n")

        speak(llama_response)

        print("-" * 50 + "\n")


if __name__ == "__main__":
    main()
