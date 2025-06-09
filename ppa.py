import sqlite3

#Creating the database
conn = sqlite3.connect("donbosko.db", check_same_thread=False)
kurkur = conn.cursor()

#Creating the table
kurkur.execute("""
               CREATE TABLE IF NOT EXISTS udus (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   password TEXT NOT NULL,
                   site TEXT NOT NULL,
                   created_at TEXT DEFAULT CURRENT_TIMESTAMP
               )
               """)
conn.commit()


#Inserting data to database
def insert_data(name,password,site,created_at=None):
    kurkur.execute("INSERT INTO udus (name, password, site) VALUES (?, ?, ?)", (name, password, site))
    kurkur.execute("SELECT id, datetime (created_at, 'local_time') AS created_at FROM udus")
    conn.commit()

def check_duplicate(name, password, site):
    kurkur.execute("SELECT COUNT(*) FROM udus WHERE name=? AND password=? AND site=?", (name, password, site))
    count = kurkur.fetchone()[0]
    return count > 0

#Getting data from database
def get_data():
    kurkur.execute("SELECT id, name, password, site, datetime(created_at, 'localtime') as created_at FROM udus")
    return kurkur.fetchall()

#Removing data from database
def delete_data_by_id(user_id):
    kurkur.execute("DELETE FROM udus WHERE id=?", (user_id,))
    conn.commit()

#Editing/updating data
def update_data(user_id, new_name, new_password):
    kurkur.execute("UPDATE udus SET name=?, password=?, created_at=CURRENT_TIMESTAMP WHERE id=?", (new_name, new_password, user_id))
    conn.commit()

#Checking duplicate data
def check_duplicate_edit(user_id, name, password, site):
    kurkur.execute("SELECT COUNT(*) FROM udus WHERE name=? AND password=? AND site=? AND id != ?", (name, password, site, user_id))
    count = kurkur.fetchone()[0]
    return count > 0