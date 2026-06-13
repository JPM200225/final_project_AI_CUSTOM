"""Modulo CAG: usa el contexto guardado para ajustar la respuesta base."""


def apply_context(user_id, question, base_answer, context_items):
    """Devuelve (respuesta_final, claves_de_contexto_usadas)."""

    context_map = {item["key"]: item["value"] for item in context_items}
    answer = base_answer
    used = []

    audience = context_map.get("audience", "")
    if "principiante" in audience.lower():
        answer += (
            " Explicacion para principiante: en palabras simples, es un "
            "mecanismo que recuerda informacion previa sobre ti para "
            "responder de forma mas personalizada."
        )
        used.append("audience")

    preferred_style = context_map.get("preferred_style", "")
    if "analogia" in preferred_style.lower():
        answer += (
            " (Piensa en esto como una libreta de notas que el asistente "
            "consulta antes de responder.)"
        )
        used.append("preferred_style")

    return answer, used
