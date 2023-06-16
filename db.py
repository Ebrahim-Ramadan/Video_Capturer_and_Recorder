import psycopg2
# from VID_CAP import *

conn = psycopg2.connect(
    host="localhost",
    database="master",
    user="postgres",
    password="sharmojj",
    port='####'  # db password
)
cursor = conn.cursor()
# alter_table_query = "ALTER TABLE Recordings ADD COLUMN Video_Content BYTEA"
# cursor.execute(alter_table_query)

# conn.commit()
# just connect your local db with this project
