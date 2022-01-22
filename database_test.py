from connect_database import *
import pandas as pd

query = """SELECT * 
            FROM users
        """

results = pd.read_sql(query, con)

print(results.to_dict('user_id'))