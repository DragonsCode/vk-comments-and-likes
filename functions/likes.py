import logging

from config import vk_user


async def get_like(id, url):
    ids = url.split('wall')[1].split('_')
    get_likes = await vk_user.api.likes.get_list(type='post', owner_id=ids[0], item_id=ids[1])
    likes = get_likes.items
    for i in likes:
        if i == id:
            return True, 'Ок'
    return False, 'Лайк не найден'


async def get_like_post(url):
    wall = None
    video = False
    try:
        wall = url.split('wall')
        if len(wall) != 2:
            raise Exception(f'Lenght of list wall (wall) is not 2, but {len(wall)}')
        
        if wall[0][-1] == '=':
            url = 'https://vk.com/wall'+wall[1]
        
        id = url[-1]
        int(id)
    except Exception as e:
        logging.error(e)

        try:
            if url[-4:] == '?c=0':
                url = url[:-4]
            
            wall = url.split('clip')
            if len(wall) != 2:
                raise Exception(f'Lenght of list wall (clip) is not 2, but {len(wall)}')
            
            if wall[0][-1] == '=':
                url = 'https://vk.com/clip'+wall[1]
            
            id = url[-1]
            int(id)
        except Exception as e:
            logging.error(e)
            return False, 'Неправильная ссылка на пост или же пост не найден'
        
        return False, 'Допускаются ссылки на посты, начинающиеся с "wall"'

    try:
        post = await vk_user.api.wall.get_by_id(posts=[wall[1]])
        type = 'group'
        author = post[0].from_id

        if author > 0:
            type = 'user'
        
        return True, type
    except Exception as e:
        logging.error(e)
        return False, 'Пост не найден или же страница с постом закрытая'