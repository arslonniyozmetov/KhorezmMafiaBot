# utils/misc/session.py

# Guruhlarga qarab sessionlarni saqlab boramiz
_sessions = {}

def get_session(chat_id: int) -> dict:
    if chat_id not in _sessions:
        _sessions[chat_id] = {
            "host_id": None,
            "players": [],
            "game_started": False,
            "roles": {},
            "night_actions": {},
            "phase": "lobby",  # yoki "night", "day", "end"
            "alive_players": [],
            "votes": {},
        }
    return _sessions[chat_id]


def reset_session(chat_id: int):
    if chat_id in _sessions:
        del _sessions[chat_id]

def get_all_sessions() -> dict:
    return _sessions

def start_game(chat_id: int):
    session = get_session(chat_id)
    session["game_started"] = True
    session["phase"] = "night"
    session["alive_players"] = list(session["players"])  # boshida barcha tirik
    session["votes"] = {}
    session["night_actions"] = {}
