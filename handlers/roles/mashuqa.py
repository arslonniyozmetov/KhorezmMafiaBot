# roles/mashuqa.py
from base import Role

class Mashuqa(Role):
    def __init__(self):
        super().__init__(
            name="Mashuqa",
            description="Tunda bir o'yinchini bloklaydi. Faol ro'l bo‘lsa, u hech nima qila olmaydi.",
            is_active=True
        )
