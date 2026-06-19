import sqlite3
import bcrypt

def create_db():
    conn = sqlite3.connect("userprofile.db")
    c = conn.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS users(
              id integer PRIMARY KEY AUTOINCREMENT, 
              username text NOT NULL UNIQUE, 
              password text NOT NULL
              )""")
    conn.commit()
    conn.close()

def save_user(new_username, new_password):
    conn = sqlite3.connect("userprofile.db")
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE username = ?", (new_username,))
    existing_user = c.fetchone()

    if existing_user is not None:
        print("That username is already taken! Please choose another one")
    else:
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt(rounds=12).decode())
        c.execute("""INSERT INTO users (username, password) VALUES (?, ?)""", (new_username, hashed_password))
        conn.commit()
        print("Successfully saved new user data!")

    conn.close()

def load_user(user_id):
    conn = sqlite3.connect("userprofile.db")
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()

    conn.close()
    
    if row is not None:
        return row[0]
    else:
        print("User Profile Not Found")

if __name__ == "__main__":
    create_db()
    