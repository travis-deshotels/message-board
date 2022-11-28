import psycopg2
import uuid




def get_query_for_get_message(get_all):
    if get_all:
        return "SELECT messageuid, SUBSTRING(message, 1, 39), poster, postedat FROM messageboard.messageboard \
                ORDER BY postedat;"
    else:
        return "SELECT * FROM (SELECT messageuid, SUBSTRING(message, 1, 39), poster, postedat \
                               FROM messageboard.messageboard ORDER BY postedat DESC LIMIT 20) AS Q \
                               ORDER BY Q.postedat ASC;"


def get_messages(get_all=False):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
        cur = conn.cursor()
        cur.execute(get_query_for_get_message(get_all))
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
        conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
        cur = conn.cursor()
        query = "SELECT message, poster, postedat FROM messageboard.messageboard WHERE messageuid = %s"
        cur.execute(query, (message_id,))
        return cur.fetchall()
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
        conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
        cur = conn.cursor()
        query = "INSERT INTO messageboard.messageboard(message, poster, postedat, messageuid) \
                 VALUES(%s, %s, NOW(), %s);"
        cur.execute(query, (message, poster, str(uuid.uuid4())[:8]))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
