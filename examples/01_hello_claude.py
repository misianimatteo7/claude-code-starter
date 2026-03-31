"""
Esempio 01 — Prima chiamata all'API di Claude.

Questo è il punto di partenza: una singola richiesta a Claude
e la lettura della risposta. Il pattern più semplice possibile.

Uso: python examples/01_hello_claude.py
"""

import os
from anthropic import Anthropic

# 1. Inizializza il client — legge ANTHROPIC_API_KEY dall'ambiente
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# 2. Crea il messaggio e invialo a Claude
response = client.messages.create(
    model="claude-haiku-4-5",   # Modello veloce per esempi semplici
    max_tokens=256,              # Lunghezza massima della risposta
    messages=[
        {"role": "user", "content": "Ciao Claude! Presentati in 2 righe."}
    ]
)

# 3. Estrai e stampa il testo della risposta
print("Risposta di Claude:")
print(response.content[0].text)

# 4. Info utili sul token usage (utile per monitorare i costi)
print(f"\nToken usati — Input: {response.usage.input_tokens}, Output: {response.usage.output_tokens}")
