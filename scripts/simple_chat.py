"""
Chat semplice con Claude — versione interattiva da terminale.

Permette di chattare con Claude direttamente dal terminale.
Digita 'exit' o 'quit' per uscire, 'clear' per resettare la conversazione.

Uso: python scripts/simple_chat.py
"""

import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def main():
    print("🤖 Claude Chat — terminale interattivo")
    print("Comandi: 'exit' per uscire, 'clear' per resettare")
    print("-" * 40)
    
    messages = []
    
    while True:
        user_input = input("\nTu: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ["exit", "quit"]:
            print("Arrivederci!")
            break
        
        if user_input.lower() == "clear":
            messages = []
            print("[Conversazione resettata]")
            continue
        
        # Aggiungi messaggio e invia
        messages.append({"role": "user", "content": user_input})
        
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            system="Sei un assistente utile, conciso e preciso.",
            messages=messages
        )
        
        reply = response.content[0].text
        messages.append({"role": "assistant", "content": reply})
        
        print(f"\nClaude: {reply}")


if __name__ == "__main__":
    main()
