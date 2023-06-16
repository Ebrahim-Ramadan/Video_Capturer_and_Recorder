import psycopg2
import bcrypt

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="master",
    user="postgres",
    password="sharmojj",
    port=7910
)

# Create a cursor object to execute database operations
cursor = conn.cursor()

# # Create a table to store user information
# create_table_query = '''
# CREATE TABLE IF NOT EXISTS Users (
#     id SERIAL PRIMARY KEY,
#     username VARCHAR(255) NOT NULL,
#     password VARCHAR(255) NOT NULL
# );
# '''
# cursor.execute(create_table_query)
# conn.commit()

# Function to register a new user


# def register(username, Password):
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
#     print("User registered successfully!")

# Function to authenticate a user


def login(username, Password):
    # Retrieve the stored Password hash for the given username
    select_query = '''
    SELECT Password FROM users WHERE username = %s;
    '''
    cursor.execute(select_query, (username,))
    result = cursor.fetchone()

    if result is not None:
        stored_Password = result[0]

        # Verify the Password
        if bcrypt.checkpw(Password.encode('utf-8'), stored_Password.encode('utf-8')):
            print("Login successful!")
        else:
            print("Invalid username or Password.")
    else:
        print("Invalid username or Password.")


# Test the login system
# register("user1", "Password123")  # Register a new user

login("user1", "Password123")  # Login with correct credentials
login("user1", "wrongPassword")  # Login with incorrect Password
login("user2", "Password123")  # Login with non-existent username

# Close the database connection
cursor.close()
conn.close()
