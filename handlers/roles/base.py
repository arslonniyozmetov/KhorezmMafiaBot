# roles/base.py

class Role:
    def __init__(self, name, description, is_mafia=False, is_active=False, is_neutral=False):
        self.name = name
        self.description = description
        self.is_mafia = is_mafia
        self.is_active = is_active
        self.is_neutral = is_neutral

    def __repr__(self):
        return self.name
