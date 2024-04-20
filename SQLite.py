import sqlite3 as sq3


def run_query(query:str, params=[]):
    con = sq3.connect('config.db')
    cur = con.cursor()
    cur.execute(query, params)
    con.commit()
    return con, cur
    
    
def create():
    query = '''CREATE TABLE IF NOT EXISTS setting (
        id INTEGER PRIMARY KEY,
        gateway TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        port INTEGER NOT NULL
        )'''
    con, cur = run_query(query=query)
    con.close()
    return cur

def count_record():
    query = '''SELECT COUNT(*) FROM setting'''
    con, cur = run_query(query=query)
    result = cur.fetchone()
    con.close()
    return result
    
def insert(gateway:str, username:str, password:str, port:int):
    query = '''INSERT INTO setting (id, gateway, username, password, port) VALUES (?, ?, ?, ?, ?)'''
    con, cur = run_query(query=query, params=[1, gateway, username, password, port])
    con.close()

def search():
    query = '''SELECT * FROM setting WHERE id=?'''
    con, cur = run_query(query=query, params=[1,])
    result = cur.fetchall()
    con.close()
    return result

def update():
    return

def delete():
    return