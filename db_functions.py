import os
from mysql.connector import connect, Error

def start_database():
    db = connect(
            host='bsuvufmpxye5uuutqete-mysql.services.clever-cloud.com',
            user='umjpzdqlwm5z2ht6',
            password= os.environ['MYSQL_PW'],
            database='bsuvufmpxye5uuutqete'
    )
    print(db)
    return(db)

def __execute_sql(cursor, sql, val=None):
    try:
        if val:
            print(sql)
            print(val)
            cursor.execute(sql, val)
        else:
            print(sql)
            cursor.execute(sql)
        return 1
    except mysql.connector.OperationalError as e:            
        if e[0] == 2006:
            start_database()
            return 0