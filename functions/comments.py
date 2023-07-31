import re

from config import vk_user


async def get_comment(id, url):
    ids = url.split('wall')[1].split('_')
    get_coms = await vk_user.api.wall.get_comments(owner_id=ids[0], post_id=ids[1], need_likes=0, sort='desc')
    comments = get_coms.items
    com = False
    for i in comments:
        if i.from_id == id:
            com = True
            words = [j for j in re.findall(r'\w+', i.text) if len(j) > 3]
            if len(words) >= 5:
                return True, i.text
    if com:
        return False, 'Комментарий слишком короткий'
    return False, 'Комментарий не найден'


async def get_post(url):
    wall = None
    post = None
    try:
        wall = url.split('wall')
        if wall[0][-1] == '=':
            url = 'https://vk.com/wall'+wall[1]
        id = url[-1]
        int(id)
    except Exception as e:
        return False, 'Неправильная ссылка на пост'
    try:
        post = await vk_user.api.wall.get_by_id(posts=[wall[1]])
    except Exception as e:
        return False, 'Пост не найден или же страница с постом закрытая'
    type = 'group'
    author = post[0].from_id
    if author > 0:
        type = 'user'

    return True, type