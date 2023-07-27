from dataclasses import dataclass

@dataclass
class User:
    id: int
    user_id: int
    posts: int
    likes: int
    
    def __str__(self):
        res = f'Your profile:\n\nUser ID: {self.user_id}\nPosts: {self.posts}\nLikes: {self.likes}'
        return res
    
    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"posts={self.posts}, "
            f"likes={self.likes}, "
            f")>"
        )


@dataclass
class Post:
    id: int
    user_id: int
    link: str
    count: int
    
    def __str__(self):
        return f'{self.link} - {self.count} comments'

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"link={self.link}, "
            f")>"
        )


@dataclass
class Like:
    id: int
    user_id: int
    link: str
    count: int
    
    def __str__(self):
        return f'{self.link} - {self.count} likes'

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"link={self.link}, "
            f")>"
        )


@dataclass
class PostView:
    id: int
    user_id: int
    post_id: int
    
    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"post_id={self.post_id}, "
            f")>"
        )


@dataclass
class LikeView:
    id: int
    user_id: int
    like_id: int
    
    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"like_id={self.like_id}, "
            f")>"
        )