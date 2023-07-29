from vkbottle import CtxStorage, BaseStateGroup

ctx = CtxStorage()

class AdminData(BaseStateGroup):

    ADD = 0
    LINK = 1


class GroupData(BaseStateGroup):

    ADD_VIP = 0
    ADD = 1
    THEME = 2

class PostData(BaseStateGroup):

    POST = 0