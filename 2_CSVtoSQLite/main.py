
import sqlite3
import pandas as pd

csv_file = 'titanic.csv'
data =  pd.read_csv(csv_file)

conn = sqlite3.connect('titanic.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS titanic_tripulants (
    PassengerId INTEGER,
    Survived INTEGER
)
''')



data.to_sql('titanic_tripulants', 
            conn, 
            if_exists = 'append',
            index = False)

conn.commit()
conn.close()
