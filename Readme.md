# 🤖 Système Multi-Agents IA — CrewAI + LangChain + Ollama

> Pipeline de veille IA automatisée avec des agents spécialisés entièrement en local via Ollama — aucune clé API requise.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-≥0.80-7c5cfc?style=flat)
![LangChain](https://img.shields.io/badge/LangChain-latest-00d4aa?style=flat)
![Ollama](https://img.shields.io/badge/Ollama-local-black?style=flat)
![License](https://img.shields.io/badge/license-MIT-green?style=flat)

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Architecture](#-architecture)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Structure du projet](#-structure-du-projet)
- [Utilisation](#-utilisation)
- [Les agents](#-les-agents)
- [Orchestration séquentielle vs hiérarchique](#-orchestration-séquentielle-vs-hiérarchique)
- [Mémoire et embeddings](#-mémoire-et-embeddings)
- [Bonus — RAG avec LangChain](#-bonus--rag-avec-langchain)
- [Dépannage](#-dépannage)
- [Ressources](#-ressources)

---

## 🎯 Vue d'ensemble

Ce projet implémente un **système multi-agents IA** capable de :

- 🔍 **Collecter** automatiquement les actualités en Intelligence Artificielle via DuckDuckGo
- 📊 **Analyser** les tendances et évaluer leur impact sur l'industrie
- 📝 **Générer** un rapport de veille structuré en Markdown, prêt à être publié

Le tout tourne **100% en local** grâce à [Ollama](https://ollama.ai), sans aucune clé API ni coût d'utilisation.

### Pourquoi le multi-agents ?

Un seul LLM atteint rapidement ses limites sur des tâches complexes (fenêtre de contexte, spécialisation). En décomposant le travail en agents spécialisés, on obtient :

| Approche | Qualité | Coût | Contrôle |
|---|---|---|---|
| LLM unique | ⚡ Rapide | 💚 Faible | 🔴 Limité |
| Multi-agents | ✅ Meilleure | 🟡 Modéré | ✅ Total |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────┐
│                    CrewAI Crew                      │
│              (Process.sequential)                   │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │   AI Scout   │→ │   Analyst    │→ │ Reporter  │ │
│  │              │  │              │  │           │ │
│  │ Collecte les │  │ Identifie    │  │ Rédige le │ │
│  │ actualités   │  │ tendances    │  │ rapport   │ │
│  │ via search   │  │ & impact     │  │ Markdown  │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
│         │                                    │      │
│  [DuckDuckGo Tool]              [rapport_veille.md] │
└─────────────────────────────────────────────────────┘
                        │
              ┌─────────▼────────┐
              │  Ollama (local)  │
              │  mistral:7b      │
              └──────────────────┘
```

### Flux d'exécution

```
Lancement → AI Scout cherche → Analyst analyse → Reporter rédige → rapport.md
              (Task 1)            (Task 2)           (Task 3)
```

---

## ✅ Prérequis

- **Python** 3.10 ou supérieur
- **Ollama** installé et en cours d'exécution
- **8 Go de RAM** minimum (16 Go recommandés)
- Connexion internet (pour DuckDuckGo Search)

---

## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/makhtar7186/multiagent-veille-ia.git
cd multiagent-veille-ia
```

### 2. Créer un environnement virtuel

```bash
python -m venv myenv

# Linux / macOS
source myenv/bin/activate

# Windows
myenv\Scripts\activate
```

### 3. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

> **Note** : Ne pas installer `langchain-ollama` séparément pour l'intégration CrewAI. Depuis CrewAI ≥ 0.80, utilisez la classe `LLM` native (voir [Configuration](#-configuration)).

### 4. Installer et configurer Ollama

```bash
# Linux / macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Windows : télécharger l'installateur sur https://ollama.ai
```

```bash
# Télécharger le modèle principal
ollama pull mistral

# Optionnel : pour la mémoire persistante
ollama pull nomic-embed-text

# Vérifier que le serveur tourne
ollama serve
```

---

## 🔧 Configuration

### Compatibilité CrewAI ≥ 0.80 (important)

Les versions récentes de CrewAI **n'acceptent plus** `ChatOllama` directement. Utilisez la classe `LLM` native :

```python
# ✅ Correct — CrewAI >= 0.80
from crewai import LLM

llm = LLM(
    model="ollama/mistral",            # format : "ollama/nom_modele"
    base_url="http://localhost:11434",
    temperature=0.2,
)

# ❌ Ne plus utiliser
# from langchain_ollama import ChatOllama
# llm = ChatOllama(model="mistral", ...)

# voire config/llm_config.py
```

### Modèles recommandés

| RAM disponible | Modèle recommandé | Commande |
|---|---|---|
| 8 Go | Mistral 7B | `ollama pull mistral` |
| 16 Go | LLaMA 3 8B | `ollama pull llama3` |
| 32 Go+ | LLaMA 3 70B | `ollama pull llama3:70b` |

---

## 📁 Structure du projet

```
multiagent-veille-ia/
│
├── main.py                    # Point d'entrée — lance la crew
│
├── agents/
│   ├── __init__.py
│   └── team.py                # Définition des 3 agents
│
├── tasks/
│   ├── __init__.py
│   └── workflow.py            # Définition des 3 tâches
│
├── tools/
│   ├── __init__.py
│   └── search_tools.py        # Outil de recherche web DuckDuckGo
│
├── rapport_veille_ia.md       # Rapport généré (créé à l'exécution)
├── requirements.txt
└── README.md
```

---

## 🚀 Utilisation

### Lancement de base

```bash
# S'assurer qu'Ollama tourne
ollama serve

# Dans un autre terminal
python main.py
```

### Avec mémoire persistante (optionnel)

```bash
# Prérequis : modèle d'embeddings
ollama pull nomic-embed-text
```

Puis dans `main.py`, décommenter le bloc `memory` :

```python
crew = Crew(
    agents=[ai_scout, analyst, reporter],
    tasks=[collect_task, analysis_task, report_task],
    process=Process.sequential,
    verbose=True,
    memory=True,                      # ← décommenter
    embedder={                        # ← décommenter
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",
            "base_url": "http://localhost:11434"
        }
    }
)
```

### Résultat attendu

```
🚀 Démarrage de la crew de veille IA...

[AI Scout] Recherche actualités IA...
[AI Scout] Recherche modèles LLM récents...
[Analyst]  Analyse des tendances identifiées...
[Reporter] Rédaction du rapport...

============================================================
✅ Rapport généré : rapport_veille_ia.md
============================================================
```

Le rapport final est sauvegardé dans `rapport_veille_ia.md` :

```markdown
# Rapport de Veille IA — Semaine XX

## Faits Saillants
- ...

## Actualités Détaillées
...

## Tendances & Analyse
...
```

---

## 🤖 Les agents

### AI Scout — Expert en Veille Technologique


**Responsabilités** : effectue plusieurs recherches DuckDuckGo ciblées (nouveaux modèles, agents IA, recherche académique, applications industrielles) et produit une liste structurée de 10 à 15 informations clés avec niveau d'importance.

---

### Analyst — Analyste en Intelligence Artificielle


**Responsabilités** : reçoit le résultat du Scout via `context`, identifie 3 à 5 tendances majeures, évalue leur impact à court et moyen terme, et identifie les connexions entre événements.

---

### Reporter — Rédacteur Technique Spécialisé


**Responsabilités** : synthétise la collecte et l'analyse en un rapport Markdown structuré, lisible en 5 minutes, sauvegardé automatiquement dans `rapport_veille_ia.md`.

---

## 🔀 Orchestration séquentielle vs hiérarchique

Ce projet utilise `Process.sequential` par défaut. Voici comment basculer en mode hiérarchique si besoin.

### Séquentiel (défaut)

```
AI Scout → Analyst → Reporter
```

- Ordre d'exécution **toujours fixe**
- Simple à déboguer
- Recommandé avec des modèles 7B locaux

### Hiérarchique

```
         Manager Agent
        ↙      ↓      ↘
  AI Scout  Analyst  Reporter
        ↘      ↓      ↙
         Manager valide
```

- Un **Manager LLM** planifie, délègue et revalide
- Peut re-déléguer si un résultat est insuffisant
- Recommandé avec des modèles 13B+

**Migration : seulement 2 lignes à changer dans `main.py`** :

```python
from crewai import Crew, Process, LLM

# LLM dédié au manager (peut être identique aux agents)
manager_llm = LLM(
    model="ollama/mistral",
    base_url="http://localhost:11434",
    temperature=0.1,    # faible pour plus de précision
)

crew = Crew(
    agents=[ai_scout, analyst, reporter],
    tasks=[collect_task, analysis_task, report_task],
    process=Process.hierarchical,   # ← changement 1
    manager_llm=manager_llm,        # ← changement 2
    verbose=True,
)
```

| Critère | Sequential | Hierarchical |
|---|---|---|
| Modèle 7B local | ✅ Recommandé | ⚠️ Lent |
| Qualité critique | 🟡 Correcte | ✅ Meilleure |
| Débogage | ✅ Simple | 🟡 Complexe |
| Tâches > 4 | 🟡 Acceptable | ✅ Recommandé |

---

## 🧠 Mémoire et embeddings

CrewAI supporte 3 types de mémoire activables ensemble :

```python
crew = Crew(
    ...
    memory=True,
    embedder={
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",    # modèle d'embeddings local
            "base_url": "http://localhost:11434"
        }
    }
)
```

| Type | Description | Stockage |
|---|---|---|
| Short-term | Contexte de la tâche en cours | RAM |
| Long-term | Résultats des sessions passées | SQLite + ChromaDB |
| Entity | Entités identifiées (personnes, orgs) | ChromaDB |

---

## 🙏 Ressources

| Outil | Documentation |
|---|---|
| CrewAI | [docs.crewai.com](https://docs.crewai.com) |
| Ollama | [ollama.ai](https://ollama.ai) |
| Modèles disponibles | [ollama.com/library](https://ollama.com/library) |
| DuckDuckGo Search | [github.com/deedy5/duckduckgo_search](https://github.com/deedy5/duckduckgo_search) |

---

## 📄 Licence

EMFAYE


---

<div align="center">

Fait avec ❤️ · **CrewAI**  + **Ollama**

*100% local · 0 clé API · Open Source*

</div>

---

# El Hadji Makhtar FAYE#   m u l t i a g e n t - v e i l l e - i a 
 
 