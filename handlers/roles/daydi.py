# roles/daydi.py
from base import Role

class Daydi(Role):
    def __init__(self):
        super().__init__(
            name="Daydi",
            description="Tunda kimning uyiga kirsa, u yerga kimlar kelganini (ismlarini) ko'radi.",
            is_active=True
        )
