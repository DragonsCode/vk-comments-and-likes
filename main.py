# coding=utf8
from vkbottle.bot import Message
from vkbottle import Bot

from models import db_api as db
from config import api, state_dispenser, labeler
from handlers import group_msg_labeler, admin_labeler, admin_group_labeler

labeler.load(group_msg_labeler)
labeler.load(admin_labeler)
labeler.load(admin_group_labeler)


bot = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser,
)

@bot.on.message(text="/id")
async def get_id(message: Message):
    await message.answer(f'peer_id: {message.peer_id}')
    

db.create_tables()
bot.run_forever()