import os
from mysql.connector import connect, Error

conn = None

def start():
    global conn
    conn = connect(
            host='bsuvufmpxye5uuutqete-mysql.services.clever-cloud.com',
            user='umjpzdqlwm5z2ht6',
            password= os.environ['MYSQL_PW'],
            database='bsuvufmpxye5uuutqete'
    )

def execute_query(sql, val=None):
    try:
        cursor = conn.cursor()
        if val:
            cursor.execute(sql, val)
        else:
            cursor.execute(sql)
    except (AttributeError, Error):
        start()
        cursor = conn.cursor()
        if val:
            cursor.execute(sql, val)
        else:
            cursor.execute(sql)
    return cursor

def execute_query_dict(sql, val=None) -> dict: 
    try:
        cursor = conn.cursor(dictionary=True)
        if val:
            cursor.execute(sql, val)
        else:
            cursor.execute(sql)
    except (AttributeError, Error):
        start()
        cursor = execute_query_dict(sql, val if val else None)
    return cursor