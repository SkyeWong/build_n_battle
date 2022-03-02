import os
from mysql.connector import connect, Error
from typing import Optional

def start_database():
    db = connect(
            host='bsuvufmpxye5uuutqete-mysql.services.clever-cloud.com',
            user='umjpzdqlwm5z2ht6',
            password= os.environ['MYSQL_PW'],
            database='bsuvufmpxye5uuutqete'
    )
    return(db)

def __execute_sql(cursor, sql, val: Optional[tuple] = None):
    try:
        if val:
            cursor.execute(sql, val)
        else:
            cursor.execute(sql)
        return 1
    except mysql.connector.OperationalError as e:            
        if e[0] == 2006:
            start_database()
            if val:
                __execute_sql(cursor, sql, val)
            else: 
                __execute_sql(cursor, sql)
            return 0