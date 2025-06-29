# game/resolve_night.py
from loader import bot
from utils.helpers import get_player_name
from utils.misc.session import get_session

async def resolve_night(chat_id: int):
    session = get_session(chat_id)
    actions = session.get("night_actions", {})
    alive = session["alive_players"]
    roles = session["roles"]

    logs = []  # O‘yinga chiqariladigan xabarlar

    # O‘sha kechadagi harakatlar
    killed = None
    saved = None
    blocked = actions.get("mashuqa")   # Mashuqa kimni blokladi
    komissar_target = actions.get("komissar")
    daydi_target = actions.get("daydi")
    qotil_target = actions.get("qotil")
    don_target = actions.get("don")
    doctor_target = actions.get("doktor")

    # 🩺 Doktor biror kishini davoladi
    if doctor_target == don_target:
        saved = doctor_target
        logs.append("🩺 Doktor bir kishini davoladi.")

    # ❌ Mashuqa kimnidir blokladi – u odam harakat qila olmaydi
    blocked_roles = []
    if blocked:
        blocked_role = roles.get(int(blocked))
        if blocked_role and blocked_role.is_active:
            blocked_roles.append(blocked_role.name.lower())

    # 🔪 Don harakat qiladi (agar bloklanmagan bo‘lsa)
    if don_target and "don" not in blocked_roles:
        killed = don_target

    # ☠️ Qotil harakat qiladi (agar bloklanmagan bo‘lsa)
    if qotil_target and "qotil" not in blocked_roles:
        if not killed:
            killed = qotil_target
        elif qotil_target != don_target:
            logs.append("⚔️ Ikkita o‘lim urinish bo‘ldi!")

    # 👮 Komissar tekshiradi (agar bloklanmagan bo‘lsa)
    if komissar_target and "komissar" not in blocked_roles:
        target_role = roles.get(int(komissar_target))
        role_name = target_role.name if target_role else "Noma'lum"
        try:
            await bot.send_message(int(komissar_target), f"👮 Siz tekshirgan o‘yinchi ro‘li: <b>{role_name}</b>", parse_mode="HTML")
        except:
            pass

    # 🕵️‍♂️ Daydi kimnidir kuzatadi (agar bloklanmagan bo‘lsa)
    if daydi_target and "daydi" not in blocked_roles:
        visited = []
        for role_name, target in actions.items():
            if int(target) == int(daydi_target) and role_name != "daydi":
                visited.append(role_name.capitalize())
        text = "🔍 Siz ko‘rgan ro‘llar: " + (", ".join(visited) if visited else "Hech kim bormagan.")
        try:
            await bot.send_message(int(daydi_target), text)
        except:
            pass

    # ✅ Yakuniy o‘lim holati
    result = ""
    if killed and int(killed) != int(saved or -1):
        if int(killed) in alive:
            alive.remove(int(killed))
            session["alive_players"] = alive
            name = await get_player_name(bot, int(killed))
            result = f"🌑 Tunda <b>{name}</b> halok bo‘ldi."
        else:
            result = "🌑 Tunda o‘ldirilgan odam allaqachon o‘yindan chiqqan edi."
    else:
        result = "🌑 Tunda hech kim halok bo‘lmadi."

    logs.insert(0, result)
    return "\n".join(logs)
