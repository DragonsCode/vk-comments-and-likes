from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, KeyboardButtonColor, Text

from models import db_api as db
from config import api, state_dispenser
from states import *
from functions.pagination import show_admin_page, get_total_pages

rules.PayloadContainsRule({'admin': 'next'})

admin_labeler = BotLabeler()
admin_labeler.vbml_ignore_case = True
admin_labeler.auto_rules = [rules.PeerRule(from_chat=False)]


@admin_labeler.private_message(text='!menu')
@admin_labeler.private_message(payload={'admin': 'menu'})
async def admin_menu(message: Message):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if message.peer_id not in admin_ids:
        return

    keyboard = Keyboard(inline=True)

    keyboard.add(Text('Группы', {'admin': 'groups'}))
    keyboard.row()
    keyboard.add(Text('Админы', {'admin': 'admins'}))

    await message.answer('Меню админа', keyboard=keyboard)


@admin_labeler.private_message(text='admin')
@admin_labeler.private_message(payload={'admin': 'admins'})
async def admins(message: Message):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if message.peer_id not in admin_ids:
        return
    
    await show_admin_page(1, message.peer_id)

@admin_labeler.message(rules.PayloadContainsRule({'admin': 'pages'}))
async def admin_navigation_handler(message: Message):
    page = int(message.get_payload_json().get('page', 0))
    if page == 0:
        await message.answer('Страница не найдена')
        return
    
    admins = db.get_all_admins()
    
    if page > get_total_pages(admins):
        page = get_total_pages(admins)
    await show_admin_page(page, message.peer_id)

@admin_labeler.private_message(text='Добавить админа')
async def add_admin_state(message: Message):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if message.peer_id not in admin_ids:
        return
    
    ctx.set(message.peer_id, {})
    await state_dispenser.set(message.peer_id, AdminData.ADD)
    return 'Введите user ID админа'


@admin_labeler.private_message(state=AdminData.ADD)
async def delete_vip_post(message: Message):
    await state_dispenser.delete(message.peer_id)
    ctx.set(message.peer_id, {})

    if not message.text.isdigit():
        await message.answer('User ID админа должен быть числом')
        await admins(message)
        return
    
    user = await api.users.get(int(message.text))
    name = f'{user[0].first_name} {user[0].last_name}'

    inseretd = db.insert_admin(int(message.text))

    if not inseretd:
        await message.answer(f'Админ [id{message.text}|{name}] уже существует')
        await admins(message)
        return
    
    await message.answer(f'Админ [id{message.text}|{name}] добавлен')


@admin_labeler.private_message(text=['Админ <user_id> <name>', 'Админ'])
async def admin_info(message: Message, user_id=None, name=None):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if message.peer_id not in admin_ids:
        return
    
    if user_id is not None:
        if not user_id.isdigit():
            await message.answer('User ID должен быть числом')
            return
        
        admin = db.get_admin_by_user_id(int(user_id))
        if not admin:
            await message.answer('Админ с таким user ID не найден')
            return
        
        user = await api.users.get(int(user_id))
        name = f'{user[0].first_name} {user[0].last_name}'

        keyboard = Keyboard(inline=True)
        keyboard.add(Text(f'Удалить админа {user_id}'))

        await message.answer(f'[id{user_id}|{name}]\n\n{str(admin)}', keyboard=keyboard)
    else:
        await message.answer('Где user ID?')


@admin_labeler.private_message(text=['Удалить админа <user_id>', 'Удалить админа'])
async def delete_admin(message: Message, user_id=None):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if message.peer_id not in admin_ids:
        return
    
    if user_id is not None:
        if not user_id.isdigit():
            await message.answer('User ID должен быть числом')
            return
        
        admin = db.get_admin_by_user_id(int(user_id))
        if not admin:
            await message.answer('Админ с таким user ID не найден')
        
        db.delete_admin(int(user_id))

        user = await api.users.get(int(user_id))
        name = f'{user[0].first_name} {user[0].last_name}'

        await message.answer(f'Админ [id{user_id}|{name}] был удалён:\n{str(admin)}')
    else:
        await message.answer('Где user ID?')