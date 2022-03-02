import os
from mysql.connector import connect, Error

conn = None

def start():
    db = connect(
            host='bsuvufmpxye5uuutqete-mysql.services.clever-cloud.com',
            user='umjpzdqlwm5z2ht6',
            password= os.environ['MYSQL_PW'],
            database='bsuvufmpxye5uuutqete'
    )
    print(db)
    return(db)

def execute(self, sql):
    try:
      cursor = conn.cursor()
      cursor.execute(sql)
    except (AttributeError, MySQLdb.OperationalError):
      connect()
      cursor = conn.cursor()
      cursor.execute(sql)
    return cursor