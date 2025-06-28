from .groups import register_group_handlers
from .users import register_user_handlers
# from .errors import register_error_handlers

def register_all_handlers(dp):
    register_user_handlers(dp)
    register_group_handlers(dp)
    # register_error_handlers(dp)
