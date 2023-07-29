from config import api

async def get_group(group_id: int):
    try:
        group = await api.messages.get_conversations_by_id(peer_ids=[group_id])
    except Exception as e:
        return False, e

    if group.items:
        return group.items[0], 0
    else:
        return False, 'cannot find group'