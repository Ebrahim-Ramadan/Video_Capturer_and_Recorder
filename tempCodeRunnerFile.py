ername, Password):
#     # Generate a salt and hash the Password
#     salt = bcrypt.gensalt()
#     hashed_Password = bcrypt.hashpw(Password.encode('utf-8'), salt)

#     # Insert the user into the database
#     insert_query = '''
#     INSERT INTO users (username, Password)
#     VALUES (%s, %s);
#     '''
#     cursor.execute(insert_query, (username, hashed_Password))
#     conn.commit()
#     print("User r