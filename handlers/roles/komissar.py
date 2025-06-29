# roles/komissar.py
from base import Role

class Komissar(Role):
    def __init__(self):
        super().__init__(
            name="Komissar",
            description="Har tunda bir o'yinchining ro'lini tekshiradi.",
            is_active=True
        )
