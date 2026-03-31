"""
Chat con risposta in streaming.

Con lo streaming, i token appaiono man mano che Claude li genera,
come su claude.ai. Essenziale per risposte lunghe e UX fluida.

Uso: python scripts/streaming_chat.py
"""

import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def stream_response(messages: list, system: str = "") -> str:
    """
    Invia una richiesta e stampa la risposta token per token.
    
    Returns:
        Testo completo della risposta
    """
    full_response = ""
    
    # context manager 'with' gestisce automaticamente lo stream
    with client.messages.stream(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        system=system,
        messages=messages
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)  # Stampa senza newline, in tempo reale
            full_response += text
    
    print()  # Newline finale
    return full_response


def main():
    print("🌊 Claude Streaming Chat")
    print("Risposta in tempo reale, token per token")
    print("-" * 40)
    
    messages = []
    
    while True:
        user_input = input("\nTu: ").strip()
        
        if not user_input or user_input.lower() in ["exit", "quit"]:
            break
        
        messages.append({"role": "user", "content": user_input})
        
        print("\nClaude: ", end="")
        reply = stream_response(messages)
        
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
