from dataclasses import dataclass


@dataclass
class Group:
    id: int
    group_id: int
    theme: str

    def __str__(self):
        themes = {0: 'comments', 1: 'likes'}
        res = f'Group info:\n\nGroup ID: {self.group_id}\nTheme: {themes[self.theme]}'
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
        res = f'Admin info:\n\nUser ID: {self.user_id}\nAdmin ID: {self.id}'
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