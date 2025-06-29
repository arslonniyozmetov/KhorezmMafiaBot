# roles/distributor.py

import random
from handlers.roles.base import Role

def distribute_roles(players):
    count = len(players)
    roles = []

    if count == 4:
        roles = [
            Role("Don", "Mafiyaning boshlig‘i. Har tun kimnidir o‘ldiradi.", is_mafia=True, is_active=True),
            Role("Doktor", "Tunda bir kishini davolay oladi.", is_active=True),
            Role("Tinch aholi", "Hech qanday kuchga ega emas."),
            Role("Tinch aholi", "Hech qanday kuchga ega emas."),
        ]
    elif count == 5:
        roles = [
            Role("Don", "Mafiyaning boshlig‘i.", is_mafia=True, is_active=True),
            Role("Doktor", "Davolaydi.", is_active=True),
            Role("Tinch aholi", ""),
            Role("Tinch aholi", ""),
            Role("Tinch aholi", ""),
        ]
    elif count == 6:
        roles = [
            Role("Don", "", is_mafia=True, is_active=True),
            Role("Doktor", "", is_active=True),
            Role("Komissar", "Kimnidir tekshiradi.", is_active=True),
            Role("Tinch aholi", ""),
            Role("Tinch aholi", ""),
            Role("Tinch aholi", ""),
        ]
    # Qo‘shimcha holatlar: 7, 8, 9, 10 — keyinchalik yozib chiqiladi.

    random.shuffle(players)
    random.shuffle(roles)
    return {player: role for player, role in zip(players, roles)}
