import os
from mysql.connector import connect, Error
db = connect(
        host='bsuvufmpxye5uuutqete-mysql.services.clever-cloud.com',
        user='umjpzdqlwm5z2ht6',
        password= os.environ['MYSQL_PW'],
        database='bsuvufmpxye5uuutqete'
)
print(db)