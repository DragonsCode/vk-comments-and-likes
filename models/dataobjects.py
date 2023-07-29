from dataclasses import dataclass


@dataclass
class Group:
    id: int
    group_id: int
    theme: str

    def __str__(self):
        themes = {0: 'комментарии', 1: 'лайки'}
        res = f'Информация о группе:\nID: {self.id}\nID группы: {self.group_id}\nТема: {themes[self.theme]}'
        return res
    
    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"group_id={self.group_id}, "
            f"theme={self.theme}, "
            f")>"
        )


@dataclass
class Admin:
    id: int
    user_id: int

    def __str__(self):
        res = f'Информация об админе:\n\nID: {self.id}\nUser ID: {self.user_id}'
        return res
    
    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"user_id={self.group_id}, "
            f")>"
        )


@dataclass
class Post:
    id: int
    group_id: int
    link: str
    vip: int
    
    def __str__(self):
        return f'{self.link}'

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"user_id={self.group_id}, "
            f"link={self.link}, "
            f"vip={self.vip}, "
            f")>"
        )