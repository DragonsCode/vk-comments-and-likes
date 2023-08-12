from vkbottle import Keyboard, Text, KeyboardButtonColor, Callback

from config import api
from models import db_api as db
from functions.group import get_group


def get_total_pages(products): 
    return (len(products) + 2) // 3  # Расчет общего количества страниц


async def show_admin_page(page: int, peer_id: int):
    admins = db.get_all_admins()

    total_pages = get_total_pages(admins)

    start_index = (page - 1) * 3
    end_index = min(start_index + 3, len(admins))

    keyboard = Keyboard(inline=True)
    if page > 1:
        keyboard.add(Text("Назад", {'admin': 'pages', 'page': str(page - 1)}))
    if page < total_pages:
        keyboard.add(Text("Вперёд", {'admin': 'pages', 'page': str(page + 1)}))

    for i in range(start_index, end_index):
        if len(keyboard.buttons) > 0:
            keyboard.row()
        user = await api.users.get(int(admins[i].user_id))
        name = f'{user[0].first_name} {user[0].last_name}'
        keyboard.add(Text(f'Админ {admins[i].user_id} {name}', {'admin': f'{admins[i].user_id}'}))

    keyboard.row()
    keyboard.add(Text('Добавить админа', {'admins': 'add'}), color=KeyboardButtonColor.POSITIVE)
    keyboard.row()
    keyboard.add(Text('Назад', {'admin': 'menu'}), color=KeyboardButtonColor.NEGATIVE)

    await api.messages.send(
        peer_id=peer_id,
        message=f"Страница {page}/{total_pages}",
        keyboard=keyboard,
        random_id=0
    )


async def show_group_page(page: int, peer_id: int):
    groups = db.get_all_groups()

    total_pages = get_total_pages(groups)

    start_index = (page - 1) * 3
    end_index = min(start_index + 3, len(groups))

    keyboard = Keyboard(inline=True)
    if page > 1:
        keyboard.add(Text("Назад", {'group': 'pages', 'page': str(page - 1)}))
    if page < total_pages:
        keyboard.add(Text("Вперёд", {'group': 'pages', 'page': str(page + 1)}))

    for i in range(start_index, end_index):
        if len(keyboard.buttons) > 0:
            keyboard.row()
        vkgroup, err = await get_group(groups[i].group_id)
        if not vkgroup:
            db.delete_group(int(groups[i].group_id))
        else:
            keyboard.add(Callback(f'{vkgroup.chat_settings.title}', {'group': f'{groups[i].group_id}'}))

    keyboard.row()
    keyboard.add(Text('Добавить группу', {'groups': 'add'}), color=KeyboardButtonColor.POSITIVE)
    keyboard.row()
    keyboard.add(Text('Назад', {'admin': 'menu'}), color=KeyboardButtonColor.NEGATIVE)

    await api.messages.send(
        peer_id=peer_id,
        message=f"Страница {page}/{total_pages}",
        keyboard=keyboard,
        random_id=0
    )