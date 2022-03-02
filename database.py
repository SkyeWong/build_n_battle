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
    print(conn)

def execute_query(sql):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
    except (AttributeError, Error):
        start()
        cursor = conn.cursor()
        cursor.execute(sql)
    return cursor