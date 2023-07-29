from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, KeyboardButtonColor, Text

from models import db_api as db
from config import api, state_dispenser
from states import *



admin_labeler = BotLabeler()
admin_labeler.vbml_ignore_case = True
admin_labeler.auto_rules = [rules.PeerRule(from_chat=False)]


@admin_labeler.private_message(text='admin menu')
@admin_labeler.private_message(payload={'admin': 'menu'})
async def admin_menu(message: Message):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if message.peer_id not in admin_ids:
        return

    keyboard = Keyboard(inline=True)

    keyboard.add(Text('Groups', {'admin': 'groups'}))
    keyboard.add(Text('Admins', {'admin': 'admins'}))

    await message.answer('Admin menu', keyboard=keyboard)


@admin_labeler.private_message(text='admin')
@admin_labeler.private_message(payload={'admin': 'admins'})
async def admins(message: Message):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if message.peer_id not in admin_ids:
        return

    keyboard = Keyboard(inline=True)

    for i in admins:
        user = await api.users.get(int(i.user_id))
        name = f'{user[0].first_name} {user[0].last_name}'
        keyboard.add(Text(f'Admin {i.user_id} {name}', {'admin': f'{i.user_id}'}))
        keyboard.row()
    
    keyboard.add(Text('Add admin', {'admins': 'add'}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text('Back', {'admin': 'menu'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('Admins', keyboard=keyboard)


@admin_labeler.private_message(text='Add admin')
async def add_admin_state(message: Message):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if message.peer_id not in admin_ids:
        return
    
    ctx.set(message.peer_id, {})
    await state_dispenser.set(message.peer_id, AdminData.ADD)
    return 'Enter the user ID of admin'


@admin_labeler.private_message(state=AdminData.ADD)
async def delete_vip_post(message: Message):
    await state_dispenser.delete(message.peer_id)
    ctx.set(message.peer_id, {})

    if not message.text.isdigit():
        await message.answer('User ID of admin should be number')
        await admins(message)
        return
    
    user = await api.users.get(int(message.text))
    name = f'{user[0].first_name} {user[0].last_name}'

    inseretd = db.insert_admin(int(message.text))

    if not inseretd:
        await message.answer(f'Admin [id{message.text}|{name}] already in database')
        await admins(message)
        return
    
    await message.answer(f'Admin [id{message.text}|{name}] have been added')


@admin_labeler.private_message(text=['Admin <user_id> <name>', 'Admin'])
async def admin_info(message: Message, user_id=None, name=None):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if message.peer_id not in admin_ids:
        return
    
    if user_id is not None:
        if not user_id.isdigit():
            await message.answer('User ID should be anumber')
            return
        
        admin = db.get_admin_by_user_id(int(user_id))
        if not admin:
            await message.answer('There is no admin with this User ID')
        
        user = await api.users.get(int(user_id))
        name = f'{user[0].first_name} {user[0].last_name}'

        keyboard = Keyboard(inline=True)
        keyboard.add(Text(f'Delete admin {user_id}'))

        await message.answer(f'[id{user_id}|{name}]\n\n{str(admin)}', keyboard=keyboard)
    else:
        await message.answer('Where is User ID?')


@admin_labeler.private_message(text=['Delete admin <user_id>', 'Delete admin'])
async def delete_admin(message: Message, user_id=None):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if message.peer_id not in admin_ids:
        return
    
    if user_id is not None:
        if not user_id.isdigit():
            await message.answer('User ID should be anumber')
            return
        
        admin = db.get_admin_by_user_id(int(user_id))
        if not admin:
            await message.answer('There is no admin with this User ID')
        
        db.delete_admin(int(user_id))

        user = await api.users.get(int(user_id))
        name = f'{user[0].first_name} {user[0].last_name}'

        await message.answer(f'Admin [id{user_id}|{name}] deleted:\n{str(admin)}')
    else:
        await message.answer('Where is User ID?')