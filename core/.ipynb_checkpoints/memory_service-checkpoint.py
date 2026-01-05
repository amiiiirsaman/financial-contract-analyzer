from collections import defaultdict
from typing import List, Tuple


class MemoryService:
    def __init__(self):
        self._sessions = defaultdict(list)

    def add_message(self, session_id: str, role: str, content: str) -> None:
        self._sessions[session_id].append((role, content))

    def get_history(self, session_id: str) -> List[Tuple[str, str]]:
        return self._sessions[session_id]
