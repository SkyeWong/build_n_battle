#import the relevant sql library
from sqlalchemy import create_engine

# link to your database
engine = create_engine('postgresql-cylindrical-72239', echo = False)

# attach the data frame (df) to the database with a name of the table; the name can be whatever you like
df.to_sql('users', con = engine, if_exists='append')

# run a quick test 
print(engine.execute("SELECT * FROM users").fetchone())