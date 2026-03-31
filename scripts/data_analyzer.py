"""
Analizzatore di dati con Claude.

Dimostra come usare Claude per analizzare dati testuali o strutturati,
estrarre insight e generare report. Utile per automazione di report,
analisi di feedback, summarization di documenti.

Uso: python scripts/data_analyzer.py
"""

import os
import json
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Dataset di esempio: feedback clienti di un brand streetwear
SAMPLE_FEEDBACK = [
    "Hoodie fantastica, qualità premium. Il cotone è morbidissimo e lo spessore è perfetto per l'inverno. Taglia vera.",
    "Spedizione veloce ma packaging migliorabile. Il prodotto in sé è ottimo, indosso la M e veste perfetta oversize.",
    "Deluso dalla qualità dello screen print, dopo 3 lavaggi si è già sbiadito. Prezzo non giustificato.",
    "Brand underground che sa il fatto suo. Drop system interessante, crea hype. Riacquisterò al prossimo drop.",
    "Taglia piccola rispetto alle misure indicate. Consiglio di prendere una taglia in su.",
    "Materiali top, costruzione solida. Finalmente un brand italiano che non delude sulle rifiniture.",
    "Il colore in foto era diverso da quello reale. Più scuro e meno saturo. Rimborso ok ma esperienza negativa.",
    "Community bella, supporto clienti risponde in meno di 24h. Prodotto all'altezza delle aspettative."
]

def analyze_feedback(feedback_list: list) -> dict:
    """
    Analizza una lista di feedback con Claude e restituisce un report strutturato.
    
    Args:
        feedback_list: Lista di stringhe con i feedback
    
    Returns:
        Dict con l'analisi strutturata
    """
    # Prepara il testo dei feedback
    feedback_text = "\n".join([f"{i+1}. {fb}" for i, fb in enumerate(feedback_list)])
    
    prompt = f"""
Analizza questi feedback di clienti per un brand streetwear e restituisci JSON con questa struttura:
{{
  "sentiment_generale": "positivo/neutro/negativo",
  "score_medio": 0.0,
  "temi_positivi": ["tema1", "tema2"],
  "temi_negativi": ["tema1", "tema2"],
  "problemi_urgenti": ["problema1"],
  "punti_di_forza": ["punto1"],
  "raccomandazioni": ["azione1", "azione2"],
  "summary": "Riassunto in 2-3 righe"
}}

Feedback:
{feedback_text}

Rispondi SOLO con il JSON, senza markdown o spiegazioni.
"""
    
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system="Sei un analista di customer feedback. Sei preciso, oggettivo e actionable nei report.",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return json.loads(response.content[0].text)


if __name__ == "__main__":
    print("📊 Analisi feedback clienti con Claude")
    print(f"Elaboro {len(SAMPLE_FEEDBACK)} feedback...\n")
    
    analysis = analyze_feedback(SAMPLE_FEEDBACK)
    
    print(f"Sentiment generale: {analysis['sentiment_generale'].upper()}")
    print(f"Score medio: {analysis['score_medio']}/10\n")
    
    print("✅ Punti di forza:")
    for p in analysis["punti_di_forza"]:
        print(f"  • {p}")
    
    print("\n⚠️ Problemi urgenti:")
    for p in analysis["problemi_urgenti"]:
        print(f"  • {p}")
    
    print("\n💡 Raccomandazioni:")
    for r in analysis["raccomandazioni"]:
        print(f"  → {r}")
    
    print(f"\n📝 Summary: {analysis['summary']}")
