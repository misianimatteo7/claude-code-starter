"""
Esempio 02 — Usare il System Prompt.

Il system prompt definisce il ruolo, il tono e il contesto di Claude
prima ancora che l'utente parli. È lo strumento più potente per
personalizzare il comportamento del modello.

Uso: python examples/02_system_prompt.py
"""

import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Il system prompt viene passato separatamente dai messaggi
# Claude lo usa come "istruzione di base" per tutta la conversazione
system_prompt = """
Sei un esperto di streetwear e moda urbana.
Rispondi sempre in modo diretto e appassionato.
Usa un tono professionale ma accessibile.
Se non sai qualcosa, dillo chiaramente.
"""

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=512,
    system=system_prompt,          # <-- Qui passi il system prompt
    messages=[
        {"role": "user", "content": "Quali sono i trend streetwear del 2025?"}
    ]
)

print("Risposta (con system prompt):")
print(response.content[0].text)
