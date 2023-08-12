from vkbottle.bot import BotLabeler, Message, rules

import logging

from models import db_api as db
from config import api
from functions.comments import get_comment, get_post
from functions.likes import get_like, get_like_post


group_msg_labeler = BotLabeler()
group_msg_labeler.vbml_ignore_case = True
group_msg_labeler.auto_rules = [rules.PeerRule(from_chat=True)]


@group_msg_labeler.chat_message()
async def read_posts(message: Message):
    if message.action or message.from_id < 0:
        try:
            await api.messages.delete(delete_for_all=True, peer_id=message.peer_id, cmids=[message.conversation_message_id])
        except Exception as e:
            logging.error(e)
        
        return
    
    txt = message.text or "вк говно"
    user_id = message.from_id
    user = ''
    if user_id > 0:
        user = await api.users.get(user_id)
    name = 'bot' if user_id < 0 else f'{user[0].first_name} {user[0].last_name}'
    group = db.get_group_by_group_id(message.peer_id)
    themes = {0: 'комментарий, содержащий как минимум 5 слов,', 1: 'лайк'}

    if not group:
        return f'Чат не найден\n\npeer_id: {message.peer_id}'
    
    if not txt.startswith("http"):
        try:
            await api.messages.delete(delete_for_all=True, peer_id=message.peer_id, cmids=[message.conversation_message_id])
        except Exception as e:
            logging.error(e)
        
        return f'[id{user_id}|{name}] Неправильная ссылка на пост'
    
    check = get_like if group.theme else get_comment
    
    vip_posts = db.get_dating_vip_posts(message.peer_id)
    vip_done = True

    for i in vip_posts:
        vip_ok, vip_comm = await check(user_id, i.link)
        if not vip_ok:
            print(vip_comm)
            vip_done = False
    
    if vip_done:
        posts = db.get_dating_posts(message.peer_id)
        posts_done = True

        for i in posts:
            post_ok, post_comm = await check(user_id, i.link)
            if not post_ok:
                posts_done = False
        
        if posts_done:
            vip_posts_links = [i.link for i in vip_posts]
            posts_links = [i.link for i in posts]

            if message.text in vip_posts_links:
                await message.answer(f'[id{user_id}|{name}], ваша ссылка уже находится в списке VIP ссылок')
                try:
                    await api.messages.delete(delete_for_all=True, peer_id=message.peer_id, cmids=[message.conversation_message_id])
                except Exception as e:
                    logging.error(e)
                return
            elif message.text in posts_links:
                await message.answer(f'[id{user_id}|{name}], ваша ссылка уже находится в последних 5 ссылках')
                try:
                    await api.messages.delete(delete_for_all=True, peer_id=message.peer_id, cmids=[message.conversation_message_id])
                except Exception as e:
                    logging.error(e)
                return

            method = get_like_post if group.theme else get_post
            ok, comm = await method(message.text)

            if ok:
                db.insert_post(message.peer_id, message.text)
                await message.answer(f'[id{user_id}|{name}], ваша ссылка принята')
            else:
                await message.answer(f'[id{user_id}|{name}] {comm}')
                try:
                    await api.messages.delete(delete_for_all=True, peer_id=message.peer_id, cmids=[message.conversation_message_id])
                except Exception as e:
                    logging.error(e)
                return
        
        else:
            text = f'[id{user_id}|{name}], вы должны оставить {themes[group.theme]} на этих постах:\n'
            for index, i in enumerate(posts, start=1):
                text+= f'\n{index} - {i.link}'
            
            await message.answer(text)
            try:
                await api.messages.delete(delete_for_all=True, peer_id=message.peer_id, cmids=[message.conversation_message_id])
            except Exception as e:
                logging.error(e)
                return

    else:
        text = f'[id{user_id}|{name}], прежде чем начать пользоваться, вы должны оставить {themes[group.theme]} на этих VIP постах:\n'
        for index, i in enumerate(vip_posts, start=1):
            text+= f'\n{index} - {i.link}'
        
        await message.answer(text)
        try:
            await api.messages.delete(delete_for_all=True, peer_id=message.peer_id, cmids=[message.conversation_message_id])
        except Exception as e:
            logging.error(e)