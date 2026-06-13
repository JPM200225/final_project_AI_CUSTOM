from backend.knowledge import retrieve_snippets
from backend.context_store import ContextStore
from backend.cag import apply_context


context_store = ContextStore()


def answer_question(user_id, question):
    snippets = retrieve_snippets(question)
    context_items = context_store.list_for_user(user_id)

    if not snippets:
        base_answer = "No encontre informacion suficiente en la base de conocimiento del curso."
        sources = []
    else:
        source_text = " ".join(item["content"] for item in snippets)
        base_answer = f"Segun la base de conocimiento del curso: {source_text}"
        sources = [item["id"] for item in snippets]

    answer, context_used = apply_context(user_id, question, base_answer, context_items)

    return {
        "user_id": user_id,
        "answer": answer,
        "sources": sources,
        "context_used": context_used,
    }
