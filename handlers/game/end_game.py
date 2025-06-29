# game/end_game.py
from utils.misc.session import get_session

def check_win_conditions(chat_id: int):
    session = get_session(chat_id)
    alive = session["alive_players"]
    roles = session["roles"]

    mafia_alive = [pid for pid in alive if roles[pid].is_mafia]
    citizen_alive = [pid for pid in alive if not roles[pid].is_mafia and not roles[pid].is_neutral]
    killer_alive = [pid for pid in alive if roles[pid].name.lower() == "qotil"]

    if len(mafia_alive) == 0 and len(killer_alive) == 0:
        return "🟢 Tinch aholi g‘alaba qozondi!"
    if len(mafia_alive) >= len(citizen_alive):
        return "🔴 Mafiya g‘alaba qozondi!"
    if len(alive) == 1 and killer_alive:
        return "⚫ Qotil g‘alaba qozondi!"

    return None  # Hali tugamagan
