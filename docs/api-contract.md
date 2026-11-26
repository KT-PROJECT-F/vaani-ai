# API contract

The backend is the source of truth. FastAPI generates the OpenAPI spec automatically:

- Interactive docs: http://localhost:8000/docs
- Raw spec: http://localhost:8000/openapi.json

Export a copy for the frontend team after every API change:

```bash
curl http://localhost:8000/openapi.json -o docs/openapi.json
```

## Endpoints in the starter code

| Method | Path | Status |
|---|---|---|
| GET | `/health` | done |
| POST | `/api/v1/chat` | done (single turn) |
| POST | `/api/v1/voice` | done (needs `GROQ_API_KEY` or local fallback) |
| GET | `/api/v1/providers?service=&city=` | done |
| POST | `/telegram/webhook` | stub (week 6) |

## Planned (see project brief)

| Method | Path | Owner |
|---|---|---|
| POST | `/api/v1/auth/otp/request`, `/verify` | Pair 3 |
| POST | `/api/v1/image` | Pair 1 |
| GET, PATCH | `/api/v1/bookings/{id}` | Pair 3 |
| GET | `/api/v1/users/me/bookings` | Pair 3 |
| GET, POST, PATCH | `/api/v1/admin/providers` | Pair 3 |
| GET | `/api/v1/admin/metrics`, `/admin/tickets` | Pair 3 |

Rule: change `backend/app/schemas/api.py` and `frontend/src/api/types.ts` in the same PR.
