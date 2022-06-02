from src.body.bot import Bot
from src.body.model import Model
from src.body.user import User
from src.body.view import View


class Controller:
    model = Model()
    bot = Bot(model)
    user = User(model, bot)
    view = View(model)
