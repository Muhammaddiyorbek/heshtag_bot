from aiogram.fsm.state import State,StatesGroup

class HeshtagForm(StatesGroup):
    heshtag_qoshish=State()
    heshtag_qoshish_tayyor=State()
    heshtag_ochirish=State()

class ReklamaForm(StatesGroup):
    reklama=State()

class AdminForm(StatesGroup):
    admin_qoshish=State()


class KanalForm(StatesGroup):
    kanal_qoshish=State()

class ImkonForm(StatesGroup):
    imkon_tahrirlash=State()