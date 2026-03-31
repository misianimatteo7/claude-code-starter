"""
Esempio 04 — Output Strutturato (JSON).

Uno dei casi d'uso più pratici: chiedere a Claude di restituire
dati in formato JSON, facile da parsare e usare nel codice.
Utilissimo per pipeline, analisi dati e integrazione con altri sistemi.

Uso: python examples/04_structured_output.py
"""

import os
import json
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Testo da analizzare (potrebbe venire da un file, database, ecc.)
product_description = """
Hoodie oversize in cotone pesante 400gsm, colore nero lavato,
logo embroidery sul petto sinistro, vestibilità streetwear, taglia M.
Prezzo: 89 euro. Disponibile nei colori: nero, bianco vintage, army green.
"""

# Chiedi a Claude di estrarre dati strutturati
response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=512,
    system="Sei un assistente che estrae dati da descrizioni di prodotti. Rispondi SOLO con JSON valido, senza markdown o spiegazioni.",
    messages=[
        {
            "role": "user",
            "content": f"""
            Estrai i dati da questa descrizione prodotto e restituisci JSON con questa struttura:
            {{
              "tipo": "...",
              "materiale": "...",
              "grammatura": "...",
              "colore_principale": "...",
              "colori_disponibili": [...],
              "taglia": "...",
              "prezzo_eur": 0,
              "dettagli": [...]
            }}
            
            Descrizione: {product_description}
            """
        }
    ]
)

# Parsa il JSON restituito
raw_text = response.content[0].text

try:
    product_data = json.loads(raw_text)
    print("✅ Dati estratti con successo:")
    print(json.dumps(product_data, indent=2, ensure_ascii=False))
except json.JSONDecodeError as e:
    print(f"❌ Errore nel parsing JSON: {e}")
    print(f"Testo raw: {raw_text}")
