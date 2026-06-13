import json
from pathlib import Path
from threading import Lock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STORE_PATH = PROJECT_ROOT / "data" / "context_store.json"


class ContextStore:
    """Persistencia simple de contexto por usuario en un archivo JSON."""

    def __init__(self, path=STORE_PATH):
        self.path = Path(path)
        self._lock = Lock()
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text("{}", encoding="utf-8")

    def _read(self):
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _write(self, data):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def save(self, user_id, key, value):
        with self._lock:
            data = self._read()
            user_context = data.get(user_id, {})
            user_context[key] = value
            data[user_id] = user_context
            self._write(data)
            return True

    def list_for_user(self, user_id):
        with self._lock:
            data = self._read()
            user_context = data.get(user_id, {})
            return [{"key": key, "value": value} for key, value in user_context.items()]
