from .base import BaseNotifier

class ConsoleNotifier(BaseNotifier):
    async def notify(self, message: str) -> None:
        print(f"[NOTIFICATION]: {message}")
