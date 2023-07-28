# coding=utf8
from vkbottle.bot import Message
from vkbottle import Bot

from models import db_api as db
from config import api, state_dispenser, labeler
from handlers import group_msg_labeler, admin_labeler

labeler.load(group_msg_labeler)
labeler.load(admin_labeler)


bot = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser,
)

@bot.on.private_message(text=['Hello <name>', 'Hello'])
async def hello(message: Message, name=None):
    if name is not None:
        await message.answer(f'Hello to {name}')
    else:
        user = await bot.api.users.get(message.from_id)
        await message.answer(f'Hello {user[0].first_name} {user[0].last_name}')
    

db.create_tables()
bot.run_forever()