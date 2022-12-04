from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminAddUser(StatesGroup):
    """State for register new user."""
    name = State()
    id = State()
    admin = State()
