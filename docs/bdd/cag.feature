Feature: Context-Augmented Generation (CAG)
  Como usuario del asistente
  Quiero que el sistema guarde y use mi contexto
  Para recibir respuestas mas personalizadas

  Scenario: Guardar contexto de usuario
    Given un usuario identificado como "ana"
    When envia un POST a /api/context con key "preferred_style" y value "explicaciones con analogias"
    Then el sistema responde con estado 201
    And el campo "saved" es verdadero

  Scenario: Recuperar contexto guardado
    Given el usuario "ana" tiene contexto guardado previamente
    When envia un GET a /api/context?user_id=ana
    Then el sistema responde con estado 200
    And la lista de contexto incluye la clave y el valor guardados

  Scenario: Usuario nuevo sin contexto previo
    Given un usuario "nuevo" que nunca ha guardado contexto
    When envia un GET a /api/context?user_id=nuevo
    Then el sistema responde con estado 200
    And la lista de contexto esta vacia

  Scenario: Usar el contexto para influir en la respuesta
    Given el usuario "luis" guardo el contexto "audience" con valor "explicar como principiante"
    When el usuario "luis" pregunta "Que es CAG?" en /api/ask
    Then la respuesta incluye una explicacion para principiantes
    And el campo "context_used" incluye "audience"

    Scenario: Pregunta sin contexto previo no se modifica
    Given un usuario sin contexto guardado
    When pregunta "Que es RAG en el curso?" en /api/ask
    Then la respuesta se basa unicamente en la base de conocimiento
    And el campo "context_used" esta vacio
