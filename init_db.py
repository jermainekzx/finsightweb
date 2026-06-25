import sqlite3
def create_db():
    conn = sqlite3.connect("userprofile.db")
    c = conn.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS users(
              id integer PRIMARY KEY AUTOINCREMENT, 
              username text NOT NULL UNIQUE, 
              password text NOT NULL
              )""")
    c.execute(""" CREATE TABLE IF NOT EXISTS watchlist(
              id integer PRIMARY KEY AUTOINCREMENT,
              user_id integer NOT NULL,
              ticker text NOT NULL
               )""")
    conn.commit()
    conn.close()

def save_user(new_username, new_password):
    conn = sqlite3.connect("userprofile.db")
    c = conn.cursor()
    c.execute(f"SELECT username FROM users WHERE username = '{new_username}'")
    existing_user = c.fetchone()

    if existing_user is not None:
        print("That username is already taken! Please choose another one")
    else:
        c.execute(f"INSERT INTO users (username, password) VALUES ('{new_username}', '{new_password}')")
        conn.commit()
        print("Successfully saved new user data!")

    conn.close()

def load_user(user_id):
    conn = sqlite3.connect("userprofile.db")
    c = conn.cursor()
    c.execute(f"SELECT username FROM users WHERE id = {user_id}")
    row = c.fetchone()

    conn.close()
    
    if row is not None:
        return row[0]
    else:
        print("User Profile Not Found")

def add_to_watchlist(user_id, ticker):
    conn = sqlite3.connect("userprofile.db")
    c = conn.cursor()
    c.execute(f"INSERT INTO watchlist (user_id, ticker) VALUES ({user_id}, '{ticker}')")
    conn.commit()
    print(f"Added {ticker} to user {user_id}'s watchlist!")
    conn.close()

def get_watchlist(user_id):
    conn = sqlite3.connect("userprofile.db")
    c = conn.cursor()
    c.execute(f"SELECT ticker FROM watchlist WHERE user_id = {user_id}")
    rows = c.fetchall()
    conn.close()
    
    return [row[0] for row in rows]

def remove_from_watchlist(user_id, ticker):
    conn = sqlite3.connect("userprofile.db")
    c = conn.cursor()
    c.execute(f"DELETE FROM watchlist WHERE user_id = {user_id} AND ticker = '{ticker}'")
    conn.commit()
    print(f"Removed {ticker} from user {user_id}'s watchlist!")
    conn.close()

if __name__ == "__main__":
    create_db()