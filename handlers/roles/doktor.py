# roles/doktor.py
from base import Role

class Doktor(Role):
    def __init__(self):
        super().__init__(
            name="Doktor",
            description="Tunda bir kishini davolay oladi.",
            is_active=True
        )
