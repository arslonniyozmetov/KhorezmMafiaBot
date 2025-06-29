# roles/don.py
from base import Role

class Don(Role):
    def __init__(self):
        super().__init__(
            name="Don",
            description="Mafiyaning boshlig‘i. Har tunda kimnidir o‘ldiradi.",
            is_mafia=True,
            is_active=True
        )
