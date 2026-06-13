# Explicacion Tecnica - Integracion CAG

## Que se implemento

Se integro un modulo de Context-Augmented Generation (CAG) sobre el proyecto
base, que ya contaba con un flujo RAG funcional. El CAG agrega una capa de
memoria persistente por usuario que se combina con la recuperacion documental
existente.

## Componentes

1. **ContextStore (`backend/context_store.py`)**
   Almacena pares clave/valor por usuario en `data/context_store.json`.
   Usa un lock para evitar condiciones de carrera al leer/escribir.
   Metodos: `save(user_id, key, value)` y `list_for_user(user_id)`.

2. **CAG (`backend/cag.py`)**
   Funcion `apply_context(user_id, question, base_answer, context_items)`.
   Recibe la respuesta base (generada por RAG) y el contexto del usuario,
   y devuelve una respuesta ajustada junto con la lista de claves de
   contexto que se usaron (`context_used`).

   Reglas implementadas:
   - Si `audience` contiene "principiante", se agrega una explicacion
     simplificada.
   - Si `preferred_style` contiene "analogia", se agrega una analogia
     (la "libreta de notas").

3. **Asistente (`backend/assistant.py`)**
   Orquesta el flujo: RAG (knowledge.py) -> obtiene contexto (ContextStore)
   -> CAG (apply_context) -> respuesta final con `sources` y `context_used`.

## Decisiones de diseno

- **Persistencia simple en JSON**: suficiente para el alcance del proyecto,
  facil de inspeccionar y no requiere dependencias externas.
- **Separacion de responsabilidades**: RAG, almacenamiento de contexto y
  aplicacion de contexto (CAG) son modulos independientes, facilmente
  testeables por separado.
- **No se rompio el contrato existente**: `/api/ask` mantiene su forma de
  respuesta, solo se enriquece `answer` y se llena `context_used`.

## Como se complementa con RAG

RAG aporta el "que sabe el sistema" (base documental del curso). CAG aporta
el "que sabe el sistema sobre este usuario" (preferencias, nivel, proyecto).
Ambos se combinan en `assistant.answer_question` para producir una respuesta
final mas relevante y personalizada.

## Pruebas

- 3 pruebas base (preexistentes).
- 3 pruebas de contrato CAG (`tests/validation/test_cag_contract.py`).
- 4 pruebas propias adicionales (`tests/test_cag_custom.py`), cubriendo
  casos de usuario sin contexto, persistencia de multiples claves y uso de
  `preferred_style`.

Total: 10/10 pruebas pasando.
