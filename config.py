from vkbottle import API, BuiltinStateDispenser, User
from vkbottle.bot import BotLabeler


token = 'token'
user_token = 'user token'

api = API(token)
vk_user = User(token=user_token)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()

ADMIN_IDS = [549425694]