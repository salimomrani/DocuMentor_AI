# DocuMentor AI

Un expert Angular local fonctionnant 100% hors-ligne via Ollama avec une interface Streamlit.

## Fonctionnalités

- 💬 **Chat avec expert Angular** — Posez des questions en langage naturel
- 📚 **RAG (Retrieval-Augmented Generation)** — Réponses basées sur la documentation officielle
- 🔗 **Citations sources** — Chaque réponse inclut les liens vers la doc
- 💾 **Historique** — Conservez vos conversations
- 🔌 **100% hors-ligne** — Pas de dépendance externe

## Prérequis

- [Ollama](https://ollama.ai) installé
- Python 3.11+

## Installation

```bash
# 1. Cloner le projet
cd DocuMentor_AI

# 2. Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate  # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Installer les modèles Ollama
ollama pull llama3
ollama pull nomic-embed-text

# 5. Lancer Ollama
ollama serve
```

## Configuration

Copiez `.env.example` vers `.env` et adaptez si besoin :

```bash
cp .env.example .env
```

## Utilisation

### 1. Scraper la documentation Angular

```bash
python -m src scrape
```

### 2. Indexer les documents

```bash
python -m src index
```

### 3. Lancer l'interface

```bash
python -m src run
```

Ou directement :

```bash
streamlit run src/ui/app.py
```

L'application sera disponible sur http://localhost:8501

## Commandes

| Commande | Description |
|----------|-------------|
| `python -m src scrape` | Scraper la doc Angular |
| `python -m src index` | Indexer les documents |
| `python -m src run` | Lancer l'interface Streamlit |

## Structure du projet

```
src/
├── scraper/          # Scraping de la documentation
├── rag/              # Pipeline RAG
│   ├── loader.py     # Chargement des documents
│   ├── splitter.py   # Découpage en chunks
│   ├── embedder.py   # Génération des embeddings
│   ├── retriever.py  # Recherche vectorielle
│   ├── generator.py  # Génération de réponses
│   └── indexer.py    # Indexation
├── ui/               # Interface Streamlit
│   └── app.py
├── storage/          # Gestion de l'historique
│   └── history.py
└── config/
    └── settings.py   # Configuration

data/
├── chroma/           # Base vectorielle
├── history/          # Conversations sauvegardées
└── docs/             # Documentation scrapée
```

## Dépannage

- **Ollama pas connecté** : Vérifiez que `ollama serve` est en cours d'exécution
- **Pas de réponses** : Relancez `python -m src scrape` puis `python -m src index`
- **Lenteur** : Utilisez un modèle plus léger ou accélérez avec GPU

---
*Généré avec [ForgeKit](https://github.com/salimomrani/forgekit)*
