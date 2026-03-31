"""
Esempio 03 — Conversazione Multi-Turno.

Claude non ha memoria tra chiamate diverse — ogni richiesta è indipendente.
Per simulare una conversazione, devi passare l'intero storico dei messaggi
ad ogni chiamata. Questo è il pattern standard per chatbot e assistenti.

Uso: python examples/03_conversation.py
"""

import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def chat(messages: list, user_input: str) -> str:
    """
    Invia un messaggio e aggiorna lo storico della conversazione.
    
    Args:
        messages: Lista dei messaggi precedenti (storico)
        user_input: Nuovo messaggio dell'utente
    
    Returns:
        Risposta di Claude come stringa
    """
    # Aggiungi il nuovo messaggio utente allo storico
    messages.append({"role": "user", "content": user_input})
    
    # Invia l'intero storico a Claude
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        system="Sei un assistente utile e conciso.",
        messages=messages  # <-- Claude vede tutto lo storico
    )
    
    # Estrai la risposta
    assistant_reply = response.content[0].text
    
    # Aggiungi la risposta di Claude allo storico
    messages.append({"role": "assistant", "content": assistant_reply})
    
    return assistant_reply


# Dimostrazione: 3 turni di conversazione
conversation_history = []

print("=== Conversazione multi-turno ===")

# Turno 1
reply1 = chat(conversation_history, "Il mio nome è Matteo. Ricordatelo.")
print(f"Claude: {reply1}")

# Turno 2 — Claude dovrebbe ricordarsi il nome
reply2 = chat(conversation_history, "Come mi chiamo?")
print(f"\nClaude: {reply2}")

# Turno 3 — Continua la conversazione
reply3 = chat(conversation_history, "Quanti messaggi abbiamo scambiato finora?")
print(f"\nClaude: {reply3}")

print(f"\n--- Storico: {len(conversation_history)} messaggi totali ---")
