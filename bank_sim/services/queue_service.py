
from collections import deque

class BankQueue:
    def __init__(self):
        self._queue: deque[int] = deque()

    def enqueue(self, client_id: int):
        self._queue.append(client_id)

    def serve_next(self) -> int | None:
        if self._queue:
            return self._queue.popleft()
        return None

    def __len__(self):
        return len(self._queue)

    def list(self):
        return list(self._queue)
