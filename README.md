# Vaani AI 2.0

Speak a home-service request in Telugu, English, Hindi or a mix. Vaani understands it, finds a provider, books a slot and confirms in your language.

## Team

| Pair | Members | Owns |
|---|---|---|
| Pair 1: Voice and channels | Pavan, Lakshmi Prasanna | `backend/app/voice/`, `backend/app/channels/` |
| Pair 2: Agent core and evals | Hemalatha, Mathan | `backend/app/agent/`, `backend/app/llm/`, `evals/` |
| Pair 3: Backend, tools and DevOps | Rajesh, Naveen | `backend/app/api/`, `backend/app/db/`, `backend/app/tools/`, `backend/app/workers/`, CI, Docker |
| Pair 4: Frontend | Sai Divya, Sujitha | `frontend/` |

## Architecture

```
React web app / React admin / Telegram bot
                 |
          FastAPI backend
       /         |          \
 Voice service  LangGraph agent  ->  LLM router (Groq -> Gemini -> Ollama)
                 |
            Agent tools
                 |
  PostgreSQL   Redis + ARQ   Langfuse Cloud
```

See `docs/architecture.md` for details.

## Prerequisites

- Python 3.12
- Node.js 20+
- Docker Desktop
- Git

## Free accounts you need (no credit card)

| Service | Used for | Get a key |
|---|---|---|
| Groq | Main LLM and Whisper speech to text | https://console.groq.com |
| Google AI Studio | Gemini Flash (backup LLM, photo diagnosis) | https://aistudio.google.com |
| Langfuse Cloud (Hobby) | Tracing LLM calls | https://cloud.langfuse.com |
| Telegram BotFather | Telegram bot token (week 6) | Message `@BotFather` in Telegram |

The app still starts without any keys. The agent then uses a simple rule-based extractor so you can build and test everything else.

## Quick start

```bash
git clone https://github.com/KT-PROJECT-F/vaani-ai.git
cd vaani-ai
git checkout dev
cp .env.example .env          # fill in your keys

# 1. Start Postgres and Redis
docker compose up -d db redis

# 2. Backend
cd backend
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
alembic upgrade head
python ../scripts/seed_providers.py
uvicorn app.main:app --reload
# API docs: http://localhost:8000/docs

# 3. Frontend (new terminal)
cd frontend
npm install
npm run dev
# App: http://localhost:5173
```

Or run everything in Docker: `docker compose up --build`.

## Common commands

```bash
make up        # start db + redis
make test      # backend tests
make lint      # ruff + mypy
make evals     # run the eval suite
make seed      # seed providers
```

## Laptop notes

- **8 GB RAM:** use Groq and Gemini only. Keep `ENABLE_LOCAL_FALLBACKS=false`. Run only `db` and `redis` in Docker.
- **16 GB RAM:** you can set `ENABLE_LOCAL_FALLBACKS=true` and install Ollama and faster-whisper (`pip install -e ".[local]"`).
- **No laptop:** open the repo in GitHub Codespaces (green "Code" button, then "Codespaces").

## How we work

Read `CONTRIBUTING.md` before your first PR.
