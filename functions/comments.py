from config import vk_user


async def get_comment(id, url):
    ids = url.split('wall')[1].split('_')
    get_coms = await vk_user.api.wall.get_comments(owner_id=ids[0], post_id=ids[1], need_likes=0, sort='desc')
    comments = get_coms.items
    com = False
    for i in comments:
        if i.from_id == id:
            com = True
            if len(i.text) > 10:
                return True, i.text
    if com:
        return False, 'comment is too short'
    return False, 'comment not found'


async def get_post(url):
    wall = None
    try:
        wall = url.split('wall')
        if wall[0][-1] == '=':
            url = 'https://vk.com/wall'+wall[1]
        id = url[-1]
        int(id)
    except Exception as e:
        return False, 'Invalid post'
    post = await vk_user.api.wall.get_by_id(posts=[wall[1]])
    type = 'group'
    author = post[0].from_id
    if author > 0:
        type = 'user'

    return True, type