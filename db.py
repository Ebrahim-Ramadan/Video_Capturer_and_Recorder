import psycopg2
# from VID_CAP import *

conn = psycopg2.connect(
    host="localhost",
    database="master",
    user="postgres",
    password="sharmojj",
    port = '7910'
)
cursor = conn.cursor()
# alter_table_query = "ALTER TABLE Recordings ADD COLUMN Video_Content BYTEA"
# cursor.execute(alter_table_query)

# conn.commit()