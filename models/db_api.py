import sqlite3
from models.dataobjects import *

#NOTE: For group theme 1 is likes and 0 is comments

#create tables
def create_tables():
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY, group_id INTEGER NOT NULL, link TEXT NOT NULL, vip INTEGER DEFAULT 0)")
    cur.execute("CREATE TABLE IF NOT EXISTS groups(id INTEGER PRIMARY KEY, group_id INTEGER NOT NULL, theme INTEGER NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS admins(id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL)")
    con.commit()
    cur.close()
    con.close()


#admins
def get_all_admins() -> list[Admin]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM admins')
    res = res.fetchall()
    cur.close()
    con.close()

    admins = []
    for i in res:
        admins.append(Admin(*i))
    
    return admins

def get_admin_by_user_id(user_id: int) -> Admin:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM admins WHERE user_id = ?', (user_id,))
    admin = res.fetchone()
    cur.close()
    con.close()

    if not admin:
        return False
    return Admin(*admin)

def insert_admin(user_id: int):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute("SELECT * FROM admins WHERE user_id = ?", (user_id,))
    is_in_db = res.fetchone()
    if is_in_db:
        cur.close()
        con.close()
        return False
    cur.execute("INSERT INTO admins(user_id) VALUES (?)", (user_id,))
    con.commit()
    cur.close()
    con.close()
    return True

def delete_admin(user_id: int):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute("SELECT * FROM admins WHERE user_id = ?", (user_id,))
    is_in_db = res.fetchone()
    if not is_in_db:
        cur.close()
        con.close()
        return False
    cur.execute("DELETE FROM admins WHERE user_id = ?", (user_id,))
    con.commit()
    cur.close()
    con.close()
    return True


#groups
def get_all_groups() -> list[Group]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM groups')
    res = res.fetchall()
    cur.close()
    con.close()

    groups = []
    for i in res:
        groups.append(Group(*i))
    
    return groups

def get_group_by_group_id(group_id: int) -> Group:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM groups WHERE group_id = ?', (group_id,))
    group = res.fetchone()
    cur.close()
    con.close()

    if not group:
        return False
    return Group(*group)

def get_groups_by_theme(theme: int) -> list[Group]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM groups WHERE theme = ?', (theme,))
    res = res.fetchall()
    cur.close()
    con.close()

    groups = []
    for i in res:
        groups.append(Group(*i))
    
    return groups

def insert_group(group_id: int, theme: int):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute("SELECT * FROM groups WHERE group_id = ?", (group_id,))
    is_in_db = res.fetchone()
    if is_in_db:
        cur.close()
        con.close()
        return Group(*is_in_db), False
    cur.execute("INSERT INTO groups(group_id, theme) VALUES (?, ?)", (group_id, theme,))
    con.commit()
    cur.close()
    con.close()
    return 0, True

def delete_group(group_id: int):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute("SELECT * FROM groups WHERE group_id = ?", (group_id,))
    is_in_db = res.fetchone()
    if not is_in_db:
        cur.close()
        con.close()
        return False
    cur.execute('DELETE FROM posts WHERE group_id = ?', (group_id,))
    cur.execute('DELETE FROM groups WHERE group_id = ?', (group_id,))
    con.commit()
    cur.close()
    con.close()
    return True


#posts
def get_posts_by_group_id(group_id: int) -> list[Post]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM posts WHERE group_id = ?', (group_id,))
    res = res.fetchall()
    cur.close()
    con.close()

    if not res:
        return False
    
    posts = []
    for i in res:
        posts.append(Post(*i))
    return posts

def get_all_posts_in_group(group_id: int, limit: int=0, vip: int=0) -> list[Post]:
    con = sqlite3.connect('bot.db')
    cur = con.cursor()

    if limit == 0:
        res = cur.execute('SELECT * FROM posts WHERE vip = ? AND group_id = ? ORDER BY id DESC', (vip, group_id,))
    else:
        res = cur.execute('SELECT * FROM posts WHERE vip = ? AND group_id = ? ORDER BY id DESC LIMIT ?', (vip, group_id, limit,))
    
    res = res.fetchall()
    cur.close()
    con.close()

    posts = []
    for i in res:
        posts.append(Post(*i))
    
    return posts

def get_dating_vip_posts(group_id: int) -> list[Post]:
    posts = []
    res = get_all_posts_in_group(group_id, vip=1)
    for i in res:
        posts.append(i)
    return posts

def get_dating_posts(group_id: int) -> list[Post]:
    posts = []
    res = get_all_posts_in_group(group_id, limit=5)
    for i in res:
        posts.append(i)
    return posts

def insert_post(group_id: int, link: str, vip: int=0):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    cur.execute("INSERT INTO posts(group_id, link, vip) VALUES (?, ?, ?)", (group_id, link, vip,))
    con.commit()
    cur.close()
    con.close()
    return True

def delete_post(id: int):
    con = sqlite3.connect('bot.db')
    cur = con.cursor()
    res = cur.execute("SELECT * FROM posts WHERE id = ?", (id,))
    is_in_db = res.fetchone()
    if not is_in_db:
        cur.close()
        con.close()
        return False
    cur.execute('DELETE FROM posts WHERE id = ?', (id,))
    con.commit()
    cur.close()
    con.close()
    return True