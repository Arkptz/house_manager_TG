from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminAddUser(StatesGroup):
    """State for register new user."""
    name = State()
    id = State()
    permission = State()
    

class AdminAddAdmin(StatesGroup):
    """State for register new user."""
    users = State()
    id = State()

class AdminDeleteAdmin(StatesGroup):
    """State for register new user."""
    users = State()
    id = State()

class AdminRemotePermission(StatesGroup):
    """State for register new user."""
    users = State()
    id = State()
    permission = State()
