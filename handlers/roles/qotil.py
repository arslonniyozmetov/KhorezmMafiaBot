# roles/qotil.py
from .base import Role

class Qotil(Role):
    def __init__(self):
        super().__init__(
            name="Qotil",
            description="Har kecha bir kishini o‘ldiradi. Faqat o‘zi tirik qolsa yutadi.",
            is_active=True,
            is_neutral=True
        )
