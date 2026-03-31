# 🤖 Claude Code Starter

> **Tutorial pratico e completo per iniziare con Claude e Claude Code — da zero a workflow avanzati.**

Questo repository è pensato per chi vuole imparare a usare **Claude** (il modello AI di Anthropic) e **Claude Code** (l'agente di coding AI) in modo pratico, con esempi reali e commentati. Non trovi teoria fine a sé stessa: ogni sezione porta direttamente a qualcosa che puoi eseguire sul tuo computer.

---

## 📋 Indice

1. [Cos'è Claude e Claude Code](#1-cosè-claude-e-claude-code)
2. [Installazione e setup](#2-installazione-e-setup)
3. [Struttura del repository](#3-struttura-del-repository)
4. [Usare Claude via API (Python)](#4-usare-claude-via-api-python)
5. [Claude Code — Agente CLI](#5-claude-code--agente-cli)
6. [Creare un workflow con agenti](#6-creare-un-workflow-con-agenti)
7. [Come usare questo repository](#7-come-usare-questo-repository)
8. [Aggiungere nuovi script e agenti](#8-aggiungere-nuovi-script-e-agenti)
9. [Best practices](#9-best-practices)
10. [Risorse utili](#10-risorse-utili)

---

## 1. Cos'è Claude e Claude Code

### Claude
Claude è il modello di linguaggio sviluppato da [Anthropic](https://anthropic.com). È disponibile in diverse versioni (Haiku, Sonnet, Opus) con capacità crescenti in termini di ragionamento, velocità e costo. Puoi accedervi via:
- **Chat web**: [claude.ai](https://claude.ai)
- **API**: per integrarlo nei tuoi script e applicazioni
- **Claude Code**: l'agente CLI per il coding

### Claude Code
Claude Code è un agente AI che gira direttamente nel tuo terminale. Non è solo un chatbot: è in grado di:
- Leggere, scrivere e modificare file nel tuo progetto
- Eseguire comandi shell
- Fare ricerche nel codebase
- Gestire git (commit, branch, diff)
- Delegare task a sub-agenti specializzati
- Eseguire test e iterare automaticamente

Il flusso di lavoro di Claude Code segue tre fasi: **gather context → take action → verify results**, in un loop adattivo.

---

## 2. Installazione e Setup

### Prerequisiti
- Node.js ≥ 18 (per Claude Code CLI)
- Python ≥ 3.9 (per gli script API)
- Un account Anthropic con API key

### Installare Claude Code CLI

```bash
npm install -g @anthropic-ai/claude-code
```

Verifica l'installazione:
```bash
claude --version
```

### Configurare la API Key

Non mettere mai la API key nel codice. Usala come variabile d'ambiente:

```bash
# macOS / Linux
export ANTHROPIC_API_KEY="sk-ant-..."

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

Oppure crea un file `.env` nella root del progetto (già incluso nel `.gitignore`):
```
ANTHROPIC_API_KEY=sk-ant-...
```

### Installare le dipendenze Python

```bash
pip install -r requirements.txt
```

### Avviare Claude Code nel terminale

```bash
# Modalità interattiva (sessione di lavoro)
claude

# Inviare un task diretto
claude "Spiega il file main.py"

# Modalità non interattiva (per script/CI)
claude -p "Analizza questo codice" < script.py

# Continuare la sessione precedente
claude -c
```

---

## 3. Struttura del Repository

```
claude-code-starter/
│
├── README.md                  # Questo file — guida completa
├── requirements.txt           # Dipendenze Python
├── .gitignore                 # File ignorati da git
│
├── scripts/                   # Script pronti all'uso
│   ├── simple_chat.py         # Chat base con Claude API
│   ├── streaming_chat.py      # Chat con risposta in streaming
│   ├── data_analyzer.py       # Analisi dati con Claude
│   └── workflow_agent.py      # Agente con workflow multi-step
│
└── examples/                  # Esempi commentati passo-passo
    ├── 01_hello_claude.py     # Prima chiamata API
    ├── 02_system_prompt.py    # Usare system prompt
    ├── 03_conversation.py     # Conversazione multi-turno
    ├── 04_structured_output.py # Output strutturato (JSON)
    └── 05_agent_workflow.py   # Workflow agentico completo
```

---

## 4. Usare Claude via API (Python)

L'SDK ufficiale si installa con `pip install anthropic`. Il pattern base è sempre lo stesso:

```python
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-opus-4-6",     # oppure claude-3-5-sonnet-20241022
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Ciao Claude!"}
    ]
)

print(response.content[0].text)
```

### Modelli disponibili

| Modello | Velocità | Costo | Uso consigliato |
|---|---|---|---|
| `claude-haiku-4-5` | ⚡ Velocissimo | $ | Task semplici, bozze |
| `claude-sonnet-4-5` | 🔄 Bilanciato | $$ | Uso generale |
| `claude-opus-4-6` | 🧠 Potente | $$$ | Ragionamento complesso |

---

## 5. Claude Code — Agente CLI

### Comandi principali

| Comando | Descrizione |
|---|---|
| `claude` | Avvia sessione interattiva |
| `claude "task"` | Esegui task diretto |
| `claude -p "query"` | Modalità non interattiva |
| `claude -c` | Continua sessione precedente |
| `claude update` | Aggiorna il CLI |
| `/clear` | Pulisci la cronologia |
| `/help` | Mostra tutti i comandi |

### Il file CLAUDE.md

Creando un file `CLAUDE.md` nella root del progetto, dai istruzioni permanenti a Claude Code su come comportarsi nel tuo progetto. Esempio:

```markdown
# CLAUDE.md — Istruzioni per il progetto

## Stile di codice
- Python: PEP8, docstring su ogni funzione
- Commits: usa conventional commits (feat:, fix:, docs:)

## Struttura
- Gli script vanno in scripts/
- I test vanno in tests/

## Comandi utili
- `python scripts/workflow_agent.py` per avviare il workflow
```

### Sub-agenti

Claude Code può delegare task a sub-agenti specializzati. Per creare un sub-agente:
```bash
claude
> /agents
> Create New subagent
```
Definisci: nome (`code-reviewer`), quando usarlo, strumenti disponibili, system prompt.

---

## 6. Creare un Workflow con Agenti

Un **workflow agentico** è una sequenza di step in cui Claude esegue operazioni, controlla i risultati e procede al passo successivo. Vedi [`scripts/workflow_agent.py`](./scripts/workflow_agent.py) per l'esempio completo.

Il pattern tipico:

```
Input → [Claude analizza] → [Esegue azione] → [Verifica risultato] → Output
```

Esempio di uso con Claude Code CLI:

```bash
# Analizza il codebase e crea un report
claude "Analizza tutti i file Python in scripts/, identifica possibili bug 
e crea un file report.md con i risultati"

# Workflow multi-step
claude "1. Leggi data.csv, 2. Analizza i dati, 3. Scrivi un summary in summary.md"
```

---

## 7. Come Usare Questo Repository

### Clona il repository

```bash
git clone https://github.com/misianimatteo7/claude-code-starter.git
cd claude-code-starter
```

### Configura l'ambiente

```bash
# Installa dipendenze Python
pip install -r requirements.txt

# Imposta la API key
export ANTHROPIC_API_KEY="sk-ant-la-tua-chiave"
```

### Esegui il primo esempio

```bash
python examples/01_hello_claude.py
```

### Esplora gli esempi in ordine

```bash
python examples/01_hello_claude.py        # Prima chiamata
python examples/02_system_prompt.py       # System prompt
python examples/03_conversation.py        # Conversazione
python examples/04_structured_output.py   # Output JSON
python examples/05_agent_workflow.py      # Workflow completo
```

### Usa Claude Code CLI nel progetto

```bash
# Apri una sessione Claude Code nella cartella
claude

# Chiedi a Claude di spiegare il progetto
> Analizza la struttura del progetto e dimmi come funziona

# Chiedi di modificare o creare file
> Aggiungi una funzione in scripts/simple_chat.py che salva le conversazioni su file
```

---

## 8. Aggiungere Nuovi Script e Agenti

### Aggiungere uno script

1. Crea un nuovo file in `scripts/` o `examples/`
2. Segui il pattern degli esempi esistenti: importa `anthropic`, usa `os.environ` per la key
3. Aggiungi una docstring descrittiva in cima al file
4. Testa localmente prima di committare

### Esempio base da cui partire

```python
"""Il mio script personalizzato.

Descrizione breve di cosa fa.
Uso: python scripts/mio_script.py
"""
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def main():
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Il tuo prompt qui"}]
    )
    print(response.content[0].text)

if __name__ == "__main__":
    main()
```

---

## 9. Best Practices

- **Mai hardcodare la API key** — usa sempre variabili d'ambiente o `.env`
- **Scegli il modello giusto** — Haiku per task veloci, Sonnet per uso generale, Opus per ragionamento
- **Usa system prompt** — definisci il ruolo e il contesto di Claude all'inizio di ogni sessione
- **Imposta `max_tokens` appropriato** — troppo basso tronca le risposte, troppo alto costa inutilmente
- **Usa lo streaming** per risposte lunghe — l'utente vede i token arrivare progressivamente
- **CLAUDE.md è il tuo copilota** — tienilo aggiornato con le convenzioni del progetto
- **Dai task precisi a Claude Code** — più contesto fornisci, migliori sono i risultati
- **Usa git come checkpoint** — committa spesso quando lavori con Claude Code

---

## 10. Risorse Utili

- 📖 [Documentazione Claude Code](https://code.claude.com/docs/en/quickstart)
- 🔧 [Anthropic Python SDK](https://platform.claude.com/docs/en/api/sdks/python)
- 🧠 [Best practices agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)
- 💬 [API Reference](https://platform.claude.com/docs)
- 🎓 [Common Workflows](https://code.claude.com/docs/en/common-workflows)

---

<div align="center">
  <p>Made with ❤️ per la community Claude</p>
  <p><strong>⭐ Se trovi utile questo repo, lascia una stella!</strong></p>
</div>
