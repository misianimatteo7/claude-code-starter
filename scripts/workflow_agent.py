"""
Agente con Workflow Multi-Step — Script Principale.

Questo è l'esempio più completo del repository.
Implementa un agente che:
1. Riceve un obiettivo in input
2. Lo scompone in task
3. Esegue ogni task in sequenza
4. Accumula il contesto tra uno step e l'altro
5. Genera un output finale consolidato

È il pattern alla base di qualsiasi sistema agentico reale.

Uso: python scripts/workflow_agent.py
     python scripts/workflow_agent.py --goal "Il tuo obiettivo personalizzato"
"""

import os
import sys
from anthropic import Anthropic
from typing import Optional

# ── CONFIGURAZIONE ─────────────────────────────────────────────────────────
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Modello da usare per ogni step
# Puoi usare modelli diversi per step diversi (es. Haiku per step veloci, Sonnet per quelli complessi)
DEFAULT_MODEL = "claude-haiku-4-5"


# ── FUNZIONI CORE ──────────────────────────────────────────────────────────

def claude_call(prompt: str, system: str = "", context: str = "", model: str = DEFAULT_MODEL) -> str:
    """
    Funzione wrapper per una singola chiamata a Claude.
    
    Questa funzione è il mattone base del workflow:
    puoi chiamarla in ogni step passando il contesto accumulato.
    
    Args:
        prompt: L'istruzione per questo step specifico
        system: System prompt (definisce il ruolo di Claude)
        context: Contesto degli step precedenti
        model: Modello Claude da usare
    
    Returns:
        Testo della risposta di Claude
    """
    messages = []
    
    # Inietta il contesto precedente come primo scambio nella conversazione
    if context:
        messages.append({
            "role": "user",
            "content": f"Contesto dagli step precedenti del workflow:\n\n{context}\n\nUsalo per il prossimo step."
        })
        messages.append({
            "role": "assistant",
            "content": "Contesto ricevuto e memorizzato. Sono pronto per il prossimo step."
        })
    
    # Il prompt effettivo di questo step
    messages.append({"role": "user", "content": prompt})
    
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system or "Sei un agente preciso e metodico. Esegui esattamente ciò che ti viene chiesto.",
        messages=messages
    )
    
    return response.content[0].text


def decompose_goal(goal: str) -> list[str]:
    """
    Step 0: Scomponi l'obiettivo principale in task eseguibili.
    
    Questa è la fase di 'planning' dell'agente: prima di fare
    qualsiasi cosa, capiamo cosa dobbiamo fare e in che ordine.
    """
    prompt = f"""
Obiettivo: {goal}

Scomponi questo obiettivo in esattamente 3-4 task sequenziali e concreti.
Ogni task deve essere:
- Specifico e misurabile
- Eseguibile autonomamente
- Costruito sul risultato del task precedente

Rispondi con una lista numerata, un task per riga, senza spiegazioni extra.
Esempio formato:
1. Analizza X
2. Crea Y basandoti su X
3. Verifica Z
"""
    
    result = claude_call(prompt)
    
    # Parsa la lista numerata
    tasks = []
    for line in result.strip().split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            # Rimuovi il numero e il punto: "1. Task" → "Task"
            task_text = line.split(".", 1)[1].strip() if "." in line else line
            tasks.append(task_text)
    
    return tasks


def execute_workflow(goal: str, verbose: bool = True) -> dict:
    """
    Esegue il workflow completo per un dato obiettivo.
    
    Flusso:
    1. Decompose goal → lista di task
    2. Esegui ogni task in sequenza
    3. Accumula contesto tra task
    4. Genera output finale
    
    Args:
        goal: L'obiettivo da raggiungere
        verbose: Se True, stampa il progresso in tempo reale
    
    Returns:
        Dict con tasks, outputs e final_summary
    """
    workflow_results = {
        "goal": goal,
        "tasks": [],
        "outputs": {},
        "final_summary": ""
    }
    
    accumulated_context = f"OBIETTIVO PRINCIPALE: {goal}\n\n"
    
    # ── FASE 1: Planning ────────────────────────────────────────────────────
    if verbose:
        print("\n🧠 [Planning] Scomposizione dell'obiettivo in task...")
    
    tasks = decompose_goal(goal)
    workflow_results["tasks"] = tasks
    
    if verbose:
        print(f"   Identificati {len(tasks)} task:")
        for i, t in enumerate(tasks, 1):
            print(f"   {i}. {t}")
    
    # ── FASE 2: Execution ───────────────────────────────────────────────────
    for i, task in enumerate(tasks, 1):
        if verbose:
            print(f"\n⚙️  [Task {i}/{len(tasks)}] {task}")
        
        # Esegui il task con il contesto accumulato fino a ora
        task_prompt = f"""
Esegui questo task specifico:
{task}

Sii preciso, dettagliato e actionable.
Il risultato verrà usato nel task successivo.
"""
        
        output = claude_call(
            prompt=task_prompt,
            context=accumulated_context
        )
        
        # Salva l'output e aggiungilo al contesto
        workflow_results["outputs"][f"task_{i}"] = output
        accumulated_context += f"=== OUTPUT TASK {i}: {task} ===\n{output}\n\n"
        
        if verbose:
            # Mostra solo le prime 2 righe dell'output per non sovraccaricare
            preview = output.split("\n")[0][:120]
            print(f"   ✅ Completato → {preview}...")
    
    # ── FASE 3: Synthesis ───────────────────────────────────────────────────
    if verbose:
        print("\n📋 [Synthesis] Generazione summary finale...")
    
    summary_prompt = f"""
Tutti i task del workflow sono stati completati.
Genera un summary finale conciso (massimo 150 parole) che:
1. Conferma il raggiungimento dell'obiettivo
2. Elenca i 3 risultati chiave
3. Suggerisce il prossimo passo logico

Obiettivo originale: {goal}
"""
    
    workflow_results["final_summary"] = claude_call(
        prompt=summary_prompt,
        context=accumulated_context
    )
    
    return workflow_results


# ── MAIN ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Leggi l'obiettivo da argomento CLI, oppure usa il default
    if len(sys.argv) > 2 and sys.argv[1] == "--goal":
        goal = " ".join(sys.argv[2:])
    else:
        # Obiettivo di default — modificalo con il tuo!
        goal = "Creare una strategia di lancio per un brand streetwear su Instagram"
    
    print("\n" + "=" * 60)
    print("  CLAUDE WORKFLOW AGENT")
    print("=" * 60)
    print(f"\n🎯 Obiettivo: {goal}")
    
    # Esegui il workflow
    results = execute_workflow(goal, verbose=True)
    
    # Output finale
    print("\n" + "=" * 60)
    print("  RISULTATI FINALI")
    print("=" * 60)
    
    for i, task in enumerate(results["tasks"], 1):
        print(f"\n--- Task {i}: {task} ---")
        print(results["outputs"][f"task_{i}"])
    
    print("\n" + "=" * 60)
    print("📋 SUMMARY FINALE:")
    print("=" * 60)
    print(results["final_summary"])
    print("\n✅ Workflow completato!")
