# Backlog del Proyecto - Integracion CAG

## Historias de usuario

### HU1 - Guardar contexto de usuario
**Como** usuario del sistema
**Quiero** poder guardar informacion de contexto (preferencias, datos del proyecto)
**Para** que el asistente la recuerde en futuras consultas

**Criterios de aceptacion:**
- POST /api/context guarda key/value asociados a un user_id
- Responde 201 y {"saved": true}

### HU2 - Recuperar contexto de usuario
**Como** usuario del sistema
**Quiero** consultar el contexto que tengo guardado
**Para** verificar que informacion recuerda el sistema sobre mi

**Criterios de aceptacion:**
- GET /api/context?user_id=X devuelve 200 y la lista de pares key/value
- Usuario sin contexto previo recibe lista vacia

### HU3 - Usar contexto para mejorar respuestas (CAG)
**Como** usuario del sistema
**Quiero** que mis respuestas se adapten a mi contexto guardado
**Para** recibir explicaciones mas utiles y personalizadas

**Criterios de aceptacion:**
- /api/ask usa el contexto guardado del usuario (audience, preferred_style)
- La respuesta incluye context_used con las claves de contexto aplicadas
- Si no hay contexto, context_used es una lista vacia y la respuesta no cambia

## Estado del backlog
- HU1: Completada (Sprint 1)
- HU2: Completada (Sprint 1)
- HU3: Completada (Sprint 1)
