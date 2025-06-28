# from .start import register_start_handlers
from .roles import register_role_handlers
from .join import register_join_handlers

def register_user_handlers(dp):
    # register_start_handlers(dp)
    register_role_handlers(dp)
    register_join_handlers(dp)
