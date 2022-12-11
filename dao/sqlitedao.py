import sqlite3
import uuid


def get_query_for_get_message(number_of_messages, get_all):
    if get_all:
        return "SELECT messageuid, SUBSTRING(message, 1, 39), poster, postedat FROM messageboard \
                ORDER BY postedat;"
    else:
        return f"SELECT * FROM (SELECT messageuid, SUBSTRING(message, 1, 39), poster, postedat \
                                FROM messageboard ORDER BY postedat DESC LIMIT {number_of_messages}) AS Q \
                                ORDER BY Q.postedat ASC;"


def get_messages(number_of_messages, get_all=False):
    conn = None
    cur = None
    try:
        conn = sqlite3.connect('D:/messageboard.db')
        cur = conn.cursor()
        cur.execute(get_query_for_get_message(number_of_messages, get_all))
        return cur.fetchall()
    except Exception as e:
        print(e)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def get_message(message_id):
    conn = None
    cur = None
    try:
        conn = sqlite3.connect('D:/messageboard.db')
        query = "SELECT message, poster, postedat FROM messageboard WHERE messageuid = ?"
        cur = conn.cursor()
        cur.execute(query, (message_id,))
        return cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def post_message(message, poster):
    conn = None
    cur = None
    try:
        conn = sqlite3.connect('D:/messageboard.db')
        cur = conn.cursor()
        query = "INSERT INTO messageboard(message, poster, postedat, messageuid) \
                 VALUES(?, ?, UNIXEPOCH(), ?);"
        cur.execute(query, (message, poster, str(uuid.uuid4())[:8]))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
