"""
Esempio 05 — Workflow Agentico Completo.

Questo è l'esempio più avanzato: un agente che esegue più step
in sequenza, dove ogni step usa l'output del precedente.
Il pattern è: analizza → pianifica → esegui → verifica.

In questo caso: analizza un'idea di business → crea un piano → valuta i rischi.

Uso: python examples/05_agent_workflow.py
"""

import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def run_step(prompt: str, context: str = "", model: str = "claude-haiku-4-5") -> str:
    """
    Esegue un singolo step del workflow.
    
    Args:
        prompt: L'istruzione per questo step
        context: Output degli step precedenti (contesto)
        model: Modello Claude da usare
    
    Returns:
        Output dello step come stringa
    """
    messages = []
    
    # Se c'è contesto dagli step precedenti, includilo
    if context:
        messages.append({
            "role": "user",
            "content": f"Contesto degli step precedenti:\n\n{context}"
        })
        messages.append({
            "role": "assistant",
            "content": "Ho letto il contesto. Procedo con il task."
        })
    
    # Aggiungi il prompt di questo step
    messages.append({"role": "user", "content": prompt})
    
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=messages
    )
    
    return response.content[0].text


def run_business_analysis_workflow(business_idea: str) -> dict:
    """
    Workflow completo in 3 step per analizzare un'idea di business.
    
    Step 1: Analisi dell'idea
    Step 2: Piano d'azione
    Step 3: Analisi dei rischi
    """
    results = {}
    accumulated_context = ""
    
    print("🔄 Avvio workflow di analisi business...\n")
    
    # ── STEP 1: Analisi dell'idea ──────────────────────────────────────────
    print("[Step 1/3] Analisi dell'idea di business...")
    
    step1_prompt = f"""
    Analizza questa idea di business in modo conciso e strutturato:
    
    IDEA: {business_idea}
    
    Fornisci:
    - Target di mercato
    - Proposta di valore unica
    - Canali di distribuzione potenziali
    - Stima dimensione mercato (piccolo/medio/grande)
    """
    
    results["analisi"] = run_step(step1_prompt)
    accumulated_context += f"=== ANALISI ===\n{results['analisi']}\n\n"
    print(f"✅ Step 1 completato ({len(results['analisi'])} caratteri)\n")
    
    # ── STEP 2: Piano d'azione ─────────────────────────────────────────────
    print("[Step 2/3] Creazione piano d'azione...")
    
    step2_prompt = """
    Basandoti sull'analisi precedente, crea un piano d'azione per i primi 90 giorni.
    Organizzalo in 3 fasi da 30 giorni ciascuna.
    Ogni fase deve avere 3 azioni concrete e misurabili.
    """
    
    results["piano"] = run_step(step2_prompt, context=accumulated_context)
    accumulated_context += f"=== PIANO ===\n{results['piano']}\n\n"
    print(f"✅ Step 2 completato ({len(results['piano'])} caratteri)\n")
    
    # ── STEP 3: Analisi rischi ─────────────────────────────────────────────
    print("[Step 3/3] Analisi dei rischi...")
    
    step3_prompt = """
    Considerando l'analisi e il piano, identifica i 5 principali rischi.
    Per ogni rischio indica:
    - Probabilità (bassa/media/alta)
    - Impatto (basso/medio/alto)
    - Strategia di mitigazione in 1 frase
    """
    
    results["rischi"] = run_step(step3_prompt, context=accumulated_context)
    print(f"✅ Step 3 completato ({len(results['rischi'])} caratteri)\n")
    
    return results


# ── ESECUZIONE PRINCIPALE ──────────────────────────────────────────────────
if __name__ == "__main__":
    # Cambia questa idea con la tua!
    idea = "Brand streetwear italiano che produce capi limited edition su preordine, venduti solo online tramite drop mensili."
    
    print("=" * 60)
    print("WORKFLOW ANALISI BUSINESS — Claude Agent")
    print("=" * 60)
    print(f"\nIdea: {idea}\n")
    print("=" * 60 + "\n")
    
    # Esegui il workflow
    output = run_business_analysis_workflow(idea)
    
    # Stampa i risultati
    print("\n" + "=" * 60)
    print("RISULTATI WORKFLOW")
    print("=" * 60)
    
    print("\n📊 ANALISI:")
    print(output["analisi"])
    
    print("\n📅 PIANO 90 GIORNI:")
    print(output["piano"])
    
    print("\n⚠️ RISCHI:")
    print(output["rischi"])
    
    print("\n✅ Workflow completato con successo!")
