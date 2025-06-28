from .game import register_game_handlers
from .vote import register_vote_handlers

def register_group_handlers(dp):
    register_game_handlers(dp)
    register_vote_handlers(dp)
