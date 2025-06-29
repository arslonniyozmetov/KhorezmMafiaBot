# roles/kamikadze.py
from handlers.roles.base import Role

class Kamikadze(Role):
    def __init__(self):
        super().__init__(
            name="Kamikadze",
            description="Oddiy o‘yinchidek yashaydi. Agar ovoz berishda o‘ldirilsa, o‘zi bilan kimnidur olib ketadi.",
            is_active=False
        )
