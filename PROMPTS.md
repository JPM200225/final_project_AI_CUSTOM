## 2026-06-12 - Sprint 1 - Objetivo: Implementar el modulo CAG (guardar, recuperar y aplicar contexto)

**Prompt usado:**
> Tengo un proyecto con backend/cag.py y backend/context_store.py como placeholders, y un test de contrato en tests/validation/test_cag_contract.py que define el comportamiento esperado: guardar contexto de usuario via POST /api/context, recuperarlo via GET /api/context, y usarlo para influir en las respuestas de /api/ask. Quiero que implementes ContextStore con persistencia en JSON, la funcion apply_context en cag.py que use el contexto para ajustar la respuesta, y que integres todo en assistant.py sin romper las pruebas base existentes.

**Resumen de respuesta:**
Se implemento ContextStore con persistencia en data/context_store.json (lectura/escritura con lock para evitar condiciones de carrera). Se implemento apply_context para detectar claves de contexto (audience, preferred_style) y modificar la respuesta agregando explicaciones adaptadas. Se integro ambo en assistant.py, pasando el contexto del usuario al CAG y devolviendo context_used.

**Decision humana:**
Acepte el diseno propuesto (persistencia simple en JSON, sin base de datos externa, por ser apropiado para el alcance del proyecto). No se solicitaron cambios adicionales en esta iteracion.

**Cambios realizados:**
- backend/context_store.py (implementacion completa, antes placeholder)
- backend/cag.py (implementacion completa, antes placeholder)
- backend/assistant.py (integracion del CAG con el flujo existente)
- data/context_store.json (nuevo, se crea automaticamente)

**Verificacion aplicada:**
Se ejecuto: python -m unittest tests.base.test_base_api tests.validation.test_cag_contract -v
Resultado: 6 tests, todos OK (3 pruebas base + 3 pruebas de validacion CAG). Ver captura docs/evidencias/sprint1-cag-tests.png

## 2026-06-12 - Sprint 1 - Objetivo: Agregar pruebas propias para el modulo CAG

**Prompt usado:**
> Necesito pruebas propias adicionales para el modulo CAG que cubran: usuario sin contexto previo (retorna lista vacia y no afecta la respuesta), guardado de multiples claves de contexto para un mismo usuario, y uso de la clave preferred_style para activar la analogia en la respuesta.

**Resumen de respuesta:**
Se creo tests/test_cag_custom.py con 4 pruebas: usuario nuevo sin contexto, ask sin contexto no usa CAG, persistencia de multiples claves para un mismo usuario, y uso de preferred_style para activar la analogia en la respuesta.

**Decision humana:**
Se acepto el archivo de pruebas tal cual. Se corrigio ademas el .gitignore, que ignoraba erroneamente PROMPTS.md (se removio esa linea para asegurar que el archivo de evidencia de prompts se suba al repo).

**Cambios realizados:**
- tests/test_cag_custom.py (nuevo)
- .gitignore (se removio linea PROMPTS.md, se agrego data/context_store.json)

**Verificacion aplicada:**
python -m unittest discover -s tests -p "test_*.py" -v -> 4 tests OK.
Combinado con ejecucion previa (6 tests base+validacion OK), total 10 pruebas pasando.

## 2026-06-12 - Sprint 2 - Objetivo: BDD, documentacion final, evidencias y validacion

**Prompt usado:**
> Necesito completar el proyecto: escribir escenarios BDD en formato Gherkin para el modulo CAG, crear la carpeta docs/evidencias con explicacion de su contenido, actualizar el README.md final con arquitectura y metodologia Scrum, escribir una explicacion tecnica breve de la integracion CAG, y dejar el cierre del sprint 2 documentado.

**Resumen de respuesta:**
Se crearon docs/bdd/cag.feature con 5 escenarios (guardar contexto, recuperar contexto, usuario sin contexto, uso de contexto en respuesta, pregunta sin contexto). Se creo docs/evidencias/README.md describiendo las capturas esperadas. Se actualizo README.md con arquitectura, flujo, endpoints y metodologia Scrum. Se creo docs/explicacion-tecnica.md y docs/scrum/sprint2.md.

**Decision humana:**
Se acepto la estructura propuesta. Se verifico previamente que toda la suite (10 pruebas) pasara antes de documentar el cierre como exitoso.

**Cambios realizados:**
- docs/bdd/cag.feature (nuevo)
- docs/evidencias/README.md (nuevo)
- docs/scrum/sprint2.md (nuevo)
- docs/explicacion-tecnica.md (nuevo)
- README.md (actualizado)

**Verificacion aplicada:**
python -m unittest tests.base.test_base_api tests.validation.test_cag_contract tests.test_cag_custom -v
Resultado: Ran 10 tests - OK. Ver captura docs/evidencias/sprint2-final-tests.png
