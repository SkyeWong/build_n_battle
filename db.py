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
    return(conn)

def execute(self, sql):
    print("i'm running!")
    try:
      cursor = conn.cursor()
      cursor.execute(sql)
    except (AttributeError, MySQLdb.OperationalError):
      start()
      cursor = conn.cursor()
      cursor.execute(sql)
    return cursor