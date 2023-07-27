import sqlite3
from models.dataobjects import *


def create_tables():
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, posts INTEGER NOT NULL DEFAULT 0, likes INTEGER NOT NULL DEFAULT 0)")
    cur.execute("CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, link TEXT NOT NULL, count INTEGER NOT NULL DEFAULT 0)")
    cur.execute("CREATE TABLE IF NOT EXISTS likes(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, link TEXT NOT NULL, count INTEGER NOT NULL DEFAULT 0)")
    cur.execute("CREATE TABLE IF NOT EXISTS post_views(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, post_id INTEGER NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS like_views(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, like_id INTEGER NOT NULL)")

#users
def get_user_by_user_id(user_id: int) -> User:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = res.fetchone()
    cur.close()
    con.close()

    if not user:
        return False
    return User(*user)

def get_all_users() -> list[User]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM users')
    res = res.fetchall()
    cur.close()
    con.close()

    users = []
    for i in res:
        users.append(User(*i))
    
    return users

def insert_user(user_id: int):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    is_in_db = res.fetchall()
    if is_in_db:
        cur.close()
        con.close()
        return False
    cur.execute("INSERT INTO users(user_id) VALUES (?)", (user_id,))
    con.commit()
    cur.close()
    con.close()
    return True

def change_user_posts(user_id: int, posts: int):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    user = get_user_by_user_id(user_id)
    if not user:
        cur.close()
        con.close()
        return False
    cur.execute('UPDATE users SET posts = ? WHERE user_id = ?', (posts, user_id,))
    con.commit()
    cur.close()
    con.close()
    return True

def delete_user(user_id: int):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute('DELETE FROM post_views WHERE user_id = ?', (user_id,))
    cur.execute('DELETE FROM like_views WHERE user_id = ?', (user_id,))
    cur.execute('DELETE FROM posts WHERE user_id = ?', (user_id,))
    cur.execute('DELETE FROM likes WHERE user_id = ?', (user_id,))
    cur.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    con.commit()
    cur.close()
    con.close()
    return True


#posts
def get_posts_by_user_id(user_id: int) -> list[Post]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM posts WHERE user_id = ?', (user_id,))
    res = res.fetchall()
    cur.close()
    con.close()

    if not res:
        return False
    
    posts = []
    for i in res:
        posts.append(Post(*i))
    return posts

def get_all_posts(limit: int=0, vip: int=0) -> list[Post]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()

    if limit == 0:
        res = cur.execute('SELECT * FROM posts WHERE vip = ? ORDER BY id DESC', (vip,))
    else:
        res = cur.execute('SELECT * FROM posts WHERE vip = ? ORDER BY id DESC LIMIT ?', (vip, limit,))
    
    res = res.fetchall()
    cur.close()
    con.close()

    posts = []
    for i in res:
        posts.append(Post(*i))
    
    return posts

def get_dating_vip_posts() -> list[Post]:
    posts = []
    res = get_all_posts(vip=1)
    for i in res:
        posts.append(Post(*i))
    return posts

def get_dating_posts() -> list[Post]:
    posts = []
    res = get_all_posts(limit=5)
    for i in res:
        posts.append(Post(*i))
    return posts

def insert_post(user_id: int, link: str):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute("INSERT INTO posts(user_id, link) VALUES (?, ?)", (user_id, link,))
    con.commit()
    cur.close()
    con.close()
    return True

def delete_post(id):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute('DELETE FROM posts WHERE id = ?', (id,))
    con.commit()
    cur.close()
    con.close()
    return True


#likes
def get_likes_by_user_id(user_id: int) -> list[Like]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM likes WHERE user_id = ?', (user_id,))
    res = res.fetchall()
    cur.close()
    con.close()

    if not res:
        return False
    
    likes = []
    for i in res:
        likes.append(Like(*i))
    return likes

def get_all_likes(limit: int=0, vip: int=0) -> list[Like]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()

    if limit == 0:
        res = cur.execute('SELECT * FROM likes WHERE vip = ? ORDER BY id DESC', (vip,))
    else:
        res = cur.execute('SELECT * FROM likes WHERE vip = ? ORDER BY id DESC LIMIT ?', (vip, limit,))
    
    res = res.fetchall()
    cur.close()
    con.close()

    likes = []
    for i in res:
        likes.append(Like(*i))
    
    return likes

def get_dating_vip_likes() -> list[Like]:
    likes = []
    res = get_all_likes(vip=1)
    for i in res:
        likes.append(Like(*i))
    return likes

def get_dating_likes() -> list[Like]:
    likes = []
    res = get_all_posts(limit=5)
    for i in res:
        likes.append(Like(*i))
    return likes

def insert_like(user_id: int, link: str):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute("INSERT INTO likes(user_id, link) VALUES (?, ?)", (user_id, link,))
    con.commit()
    cur.close()
    con.close()
    return True

def delete_like(id):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute('DELETE FROM likes WHERE id = ?', (id,))
    con.commit()
    cur.close()
    con.close()
    return True


#post views
def get_post_views_by_user_id(user_id: int) -> list[PostView]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM post_views WHERE user_id = ?', (user_id,))
    views = res.fetchall()
    cur.close()
    con.close()

    views = []
    for i in views:
        views.append(PostView(*i))
    
    return views

def get_post_views_by_post_id(post_id: int) -> list[PostView]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM post_views WHERE post_id = ?', (post_id,))
    views = res.fetchall()
    cur.close()
    con.close()

    views = []
    for i in views:
        views.append(PostView(*i))
    
    return views

def insert_post_view(user_id: int, post_id: int):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute("INSERT INTO post_views(user_id, post_id) VALUES (?, ?)", (user_id, post_id,))
    con.commit()
    cur.close()
    con.close()
    return True

def delete_post_views_by_post_id(post_id: int):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute('DELETE FROM post_views WHERE post_id = ?', (post_id,))
    con.commit()
    cur.close()
    con.close()
    return True

def delete_post_views_by_user_id(user_id: int):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute('DELETE FROM post_views WHERE user_id = ?', (user_id,))
    con.commit()
    cur.close()
    con.close()
    return True


#like views
def get_like_views_by_user_id(user_id: int) -> list[LikeView]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM like_views WHERE user_id = ?', (user_id,))
    views = res.fetchall()
    cur.close()
    con.close()

    views = []
    for i in views:
        views.append(LikeView(*i))
    
    return views

def get_like_views_by_like_id(like_id: int) -> list[LikeView]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM like_views WHERE like_id = ?', (like_id,))
    views = res.fetchall()
    cur.close()
    con.close()

    views = []
    for i in views:
        views.append(LikeView(*i))
    
    return views

def insert_like_view(user_id: int, like_id: int):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute("INSERT INTO like_views(user_id, like_id) VALUES (?, ?)", (user_id, like_id,))
    con.commit()
    cur.close()
    con.close()
    return True

def delete_like_views_by_like_id(like_id: int):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute('DELETE FROM like_views WHERE like_id = ?', (like_id,))
    con.commit()
    cur.close()
    con.close()
    return True

def delete_like_views_by_user_id(user_id: int):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute('DELETE FROM like_views WHERE user_id = ?', (user_id,))
    con.commit()
    cur.close()
    con.close()
    return True