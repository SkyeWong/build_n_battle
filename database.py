import os
from mysql.connector import connect, Error

conn = None

def start():
    conn = connect(
            host='bsuvufmpxye5uuutqete-mysql.services.clever-cloud.com',
            user='umjpzdqlwm5z2ht6',
            password= os.environ['MYSQL_PW'],
            database='bsuvufmpxye5uuutqete'
    )
    print(conn)

def execute_query(sql):
    print("i'm running!")
    try:
      cursor = conn.cursor()
      cursor.execute(sql)
    except (AttributeError, Error):
      start()
      print("the database isn't started, i restarted it and now i'm gonna execute the query!")
      cursor = conn.cursor()
      print("the cursor is created, if everything works i'm gonna execute it!")
      cursor.execute(sql)
    return cursor