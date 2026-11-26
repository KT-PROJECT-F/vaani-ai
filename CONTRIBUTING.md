# Contributing

## Branches

- `main` is protected. Nobody pushes to it directly.
- Create a branch per task: `<type>/<pair>-<short-topic>`
  - `feat/p1-voice-endpoint`
  - `fix/p3-booking-double-slot`
  - `docs/p2-prompt-guide`

## Commits

Use conventional commits:

```
feat: add clarify node
fix: handle empty transcript
docs: explain eval format
test: add booking tool tests
refactor: split llm router
chore: bump dependencies
```

## Pull requests

1. One task per PR. Keep it small (under ~400 changed lines when possible).
2. Link the GitHub issue (`Closes #12`).
3. Fill in the PR template.
4. CI must be green.
5. One review from a different pair is required. Changes in `backend/app/agent/` or `backend/app/agent/prompts/` also need a mentor review.
6. The author merges after approval (squash merge).

## Definition of done

- Code merged to `main`
- Tests added or updated
- `ruff` and `mypy` pass (`eslint` for frontend)
- Docs updated if behavior changed
- Eval score is not lower than before (for agent changes)

## Rhythm

- Daily standup: 15 minutes (yesterday, today, blockers)
- Weekly demo: every Monday
- Work is tracked on the GitHub Projects board, one issue per task

## Code style

- Python: type hints everywhere, `ruff format`, small functions, no secrets in code
- Settings come from `app/core/config.py`, never `os.getenv` scattered around
- Every external call (LLM, STT, TTS, Telegram) needs a timeout and a fallback
- Frontend: TypeScript strict mode, components in `src/components/`, API calls only through `src/api/`

## Architecture decisions

Big decisions (new library, new service, schema change) get a short ADR in `docs/adr/`. Copy `0001-record-architecture-decisions.md` as a template.
