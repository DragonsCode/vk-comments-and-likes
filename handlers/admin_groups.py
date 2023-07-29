from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, KeyboardButtonColor, Text

from vkbottle.modules import json
from vkbottle import Keyboard, Callback, \
                        GroupEventType, GroupTypes

from models import db_api as db
from config import api, state_dispenser
from states import *
from functions.likes import get_like_post
from functions.comments import get_post
from functions.group import get_group


admin_group_labeler = BotLabeler()
admin_group_labeler.vbml_ignore_case = True
admin_group_labeler.auto_rules = [rules.PeerRule(from_chat=False)]


@admin_group_labeler.private_message(text='admin')
@admin_group_labeler.private_message(payload={'admin': 'groups'})
async def groups(message: Message):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if message.peer_id not in admin_ids:
        return
    
    groups = db.get_all_groups()

    keyboard = Keyboard(inline=True)

    for i in groups:
        vkgroup, err = await get_group(i.group_id)
        keyboard.add(Callback(f'{vkgroup.chat_settings.title}', {'group': f'{i.group_id}'}))
        keyboard.row()
    
    keyboard.add(Text('Add group', {'groups': 'add'}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text('Back', {'admin': 'menu'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('Groups', keyboard=keyboard)


@admin_group_labeler.private_message(text='Add group')
async def add_group_state(message: Message):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if message.peer_id not in admin_ids:
        return
    
    ctx.set(message.peer_id, {})
    await state_dispenser.set(message.peer_id, GroupData.ADD)
    return 'Enter the peer ID of group'


@admin_group_labeler.private_message(state=GroupData.ADD)
async def add_group_id(message: Message):
    if not message.text.isdigit():
        await state_dispenser.delete(message.peer_id)
        ctx.set(message.peer_id, {})
        await message.answer('Peer ID of group should be a number')
        await groups(message)
        return
    
    group = db.get_group_by_group_id(int(message.text))

    if group:
        await state_dispenser.delete(message.peer_id)
        ctx.set(message.peer_id, {})
        await message.answer('Group is already in database')
        await groups(message)
        return
    
    vkgroup, err = await get_group((int(message.text)))
    if not vkgroup:
        await state_dispenser.delete(message.peer_id)
        ctx.set(message.peer_id, {})
        await message.answer(f'Something went wrong: {err}')
        await groups(message)
        return

    ctx.set(message.peer_id, {'group_id': message.text})
    await state_dispenser.set(message.peer_id, GroupData.THEME)

    return 'Enter the theme of group\nFor group theme 1 is likes and 0 is comments'


@admin_group_labeler.private_message(state=GroupData.THEME)
async def add_group_theme(message: Message):
    if not message.text in ['0', '1', 0, 1]:
        return 'Please, enter the theme of group correctly!\nFor group theme 1 is likes and 0 is comments'
    
    data = ctx.get(message.peer_id)
    group_id = int(data['group_id'])
    theme = int(message.text)
    
    db.insert_group(group_id, theme)

    await state_dispenser.delete(message.peer_id)
    ctx.set(message.peer_id, {})

    group = db.get_group_by_group_id(group_id)

    await message.answer(f'Group added:\n\n{str(group)}')
    await groups(message)


@admin_group_labeler.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def groups_event(event: GroupTypes.MessageEvent):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if event.object.peer_id not in admin_ids:
        await api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id
        )
    
    group_id = event.object.payload.get('group', False)
    if group_id:
        group = db.get_group_by_group_id(int(group_id))
        vkgroup, err = await get_group(group.group_id)
        if not vkgroup:
            await api.messages.send(peer_id=event.object.peer_id, message=f'Something went wrong: {err}', random_id=0)
            return

        group_vip_posts = db.get_dating_vip_posts(group.group_id)

        text = f'Group {vkgroup.chat_settings.title}:\n\n{str(group)}\n\nVIP posts:'
        for i in group_vip_posts:
            text += f'\nID: {i.id} link: {i.link}'
        
        keyboard = Keyboard(inline=True)
        keyboard.add(Text('Delete post'))
        keyboard.row()
        keyboard.add(Text('Add VIP post', {'post_group_id': f'{group.group_id}'}))
        keyboard.row()
        keyboard.add(Text('Delete this group', {'del_group_id': f'{group.group_id}'}))
        keyboard.row()

        keyboard.add(Text('Back', {'admin': 'groups'}), color=KeyboardButtonColor.NEGATIVE)


        await api.messages.send(peer_id=event.object.peer_id, message=text, keyboard=keyboard, random_id=0)
        await api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id
        )

    else:
        await api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id
        )


@admin_group_labeler.private_message(text='Delete post')
async def delete_vip_post_state(message: Message):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if message.peer_id not in admin_ids:
        return
    
    ctx.set(message.peer_id, {})
    await state_dispenser.set(message.peer_id, PostData.POST)
    return 'Enter the ID of post'


@admin_group_labeler.private_message(state=PostData.POST)
async def delete_vip_post(message: Message):
    await state_dispenser.delete(message.peer_id)
    ctx.set(message.peer_id, {})

    if not message.text.isdigit():
        await message.answer('ID of post should be a number')
        await groups(message)
        return
    
    deleted = db.delete_post(int(message.text))

    if not deleted:
        await message.answer('Post not found')
        await groups(message)
        return

    await message.answer('Post deleted')
    await groups(message)


@admin_group_labeler.private_message(text='Add VIP post')
async def add_vip_post_state(message: Message):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if message.peer_id not in admin_ids:
        return
    
    try:
        group_id = message.get_payload_json().get('post_group_id', False)
    except AttributeError:
        await message.answer('I cannot see the group ID in the payload')
        await groups(message)
        return

    if not group_id:
        await message.answer('I cannot see the group ID in the payload')
        await groups(message)
        return
    
    ctx.set(message.peer_id, {'group_id': group_id})
    await state_dispenser.set(message.peer_id, GroupData.ADD_VIP)
    return 'Enter the link to the post'


@admin_group_labeler.private_message(state=GroupData.ADD_VIP)
async def add_vip_post(message: Message):
    data = ctx.get(message.peer_id)
    group = db.get_group_by_group_id(int(data['group_id']))

    await state_dispenser.delete(message.peer_id)
    ctx.set(message.peer_id, {})

    method = get_like_post if group.theme else get_post
    ok, comm = await method(message.text)

    if not ok:
        await message.answer(f'Something is wrong with this link: {comm}')
        await groups(message)
        return
    
    db.insert_post(group.group_id, message.text, 1)

    await message.answer(f'VIP post added to this group:\n\n{str(group)}')
    await groups(message)


@admin_group_labeler.private_message(text='Delete this group')
async def delete_this_group(message: Message):
    admins = db.get_all_admins()
    admin_ids = [i.user_id for i in admins]

    if message.peer_id not in admin_ids:
        return
    
    try:
        group_id = message.get_payload_json().get('del_group_id', False)
    except AttributeError:
        await message.answer('I cannot see the group ID in the payload')
        await groups(message)
        return

    if not group_id:
        await message.answer('I cannot see the group ID in the payload')
        await groups(message)
        return
    
    deleted = db.delete_group(int(group_id))

    if not deleted:
        await message.answer('Group not found')
        await groups(message)
        return

    await message.answer('Group deleted')
    await groups(message)