# Proyecto Examen Final - Modulo 3 - Integracion CAG

Proyecto base extendido con un modulo de **CAG (Context-Augmented Generation)**
que permite guardar, recuperar y usar contexto persistente del usuario para
mejorar las respuestas del asistente, complementando el flujo RAG existente.

## Arquitectura

- `backend/knowledge.py`: recuperacion de informacion (RAG) desde `data/knowledge_base.json`.
- `backend/context_store.py`: persistencia de contexto por usuario en `data/context_store.json` (JSON, con lock para concurrencia).
- `backend/cag.py`: aplica el contexto guardado del usuario para ajustar la respuesta (ej. nivel de audiencia, estilo preferido).
- `backend/assistant.py`: orquesta RAG + CAG para construir la respuesta final, devolviendo `context_used`.
- `backend/server.py`: expone los endpoints HTTP (`/health`, `/api/ask`, `/api/context`).
- `frontend/`: interfaz web estatica para interactuar con el backend.

### Flujo de una consulta

1. El usuario envia una pregunta a `/api/ask` con su `user_id`.
2. `assistant.py` recupera fragmentos relevantes de la base de conocimiento (RAG).
3. `assistant.py` recupera el contexto guardado del usuario (CAG).
4. `cag.apply_context` ajusta la respuesta base segun el contexto (ej. agrega explicacion para principiantes).
5. Se devuelve la respuesta junto con `sources` (RAG) y `context_used` (CAG).

## Inicio rapido

1. Ejecute las pruebas base y de validacion (ver abajo).
2. Levante el backend.
3. Abra el frontend para interactuar con el asistente.

## Ejecutar pruebas

```bash
python -m unittest tests.base.test_base_api tests.validation.test_cag_contract tests.test_cag_custom -v
```

Resultado esperado: 10 pruebas, todas OK.

## Ejecutar backend

```bash
PYTHONPATH=. python3 -m backend.server
```

El backend queda disponible en `http://127.0.0.1:8000`.

## Abrir frontend

Abra `frontend/index.html` en un navegador.

## Endpoints principales

- `GET /health` - estado del servidor.
- `POST /api/ask` - `{ "user_id": "...", "question": "..." }` -> respuesta usando RAG + CAG.
- `POST /api/context` - `{ "user_id": "...", "key": "...", "value": "..." }` -> guarda contexto.
- `GET /api/context?user_id=...` - lista el contexto guardado del usuario.

## Metodologia Scrum

El desarrollo se organizo en 2 sprints, documentados en `docs/scrum/`:

- **Sprint 1**: implementacion del modulo CAG (ContextStore, apply_context, integracion en assistant.py) y pruebas propias.
- **Sprint 2**: escenarios BDD, documentacion final, evidencias y validacion final.

Ver `docs/scrum/backlog.md`, `docs/scrum/sprint1.md` y `docs/scrum/sprint2.md`.

## BDD

Escenarios de comportamiento del modulo CAG en `docs/bdd/cag.feature`.

## Explicacion tecnica

Ver `docs/explicacion-tecnica.md`.

## Evidencias

Ver `docs/evidencias/` para capturas de pruebas, funcionamiento y proceso Scrum.

## Registro de uso de IA

Ver `PROMPTS.md` para el registro cronologico de prompts usados, decisiones
humanas y verificaciones aplicadas.
