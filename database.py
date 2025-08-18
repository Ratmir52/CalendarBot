import sqlite3

con = sqlite3.connect("database/database.db")
cur = con.cursor()

class DataBase():

    def __init__(self, con, cur):
        self.r_table = "reminders"
        self.g_table = "google"
        self.con = con
        self.cur = cur

    def create_table(self, name):
        cur.execute(f"CREATE TABLE {name}(id, chat_id, msg, fnsh_t, UNIQUE(id, chat_id, msg, fnsh_t))")

    def drop_table(self, name):
        cur.execute(f"DROP TABLE {name}")

    def add_reminder(self, id, chat_id, msg, fnsh_t):

        cur.execute(f"""INSERT INTO {self.r_table} VALUES (?, ?, ?, ?) ON CONFLICT(id, chat_id, msg, fnsh_t) DO NOTHING""", (id, chat_id, msg, fnsh_t))
        self.con.commit()

    def add_token(self, id, token, r_token):
        res = cur.execute(f"""INSERT INTO {self.g_table} VALUES (?, ?, ?) ON CONFLICT(id) DO UPDATE SET token = ?, r_token = ?""", (id, token, r_token, token, r_token))

        self.con.commit()

    def get_token(self, id):
        res = cur.execute(f"""SELECT * FROM {self.g_table} WHERE id = ?""", (id,))
        return cur.fetchone()

    def upd_chat(self, new_id, usr_id):
        cur.execute(f"""UPDATE {self.r_table} SET chat_id = ? WHERE id = ?""", (new_id, usr_id))
        self.con.commit()

    def remove_reminder(self, id):
        cur.execute(f"""DELETE FROM {self.r_table} WHERE id=?""", (id, ))
        self.con.commit()

    def get_user(self, id):
        res = cur.execute(f"""SELECT * FROM {self.r_table} WHERE id = ?""", (id,))
        return cur.fetchone()

    def get_google(self, data):
        if data not in ["id", "token", "r_token"]:
            return

        res = cur.execute(f"""SELECT {data} FROM google""")
        rows = res.fetchall()
        return [row[0] for row in rows]


    def get_all(self, obj):
        res = None

        if(obj == "msg"):
            res = cur.execute(f"""SELECT msg FROM reminders""")
        if (obj == "finish"):
            res = cur.execute(f"""SELECT fnsh_t FROM reminders""")
        if (obj == "id"):
            res = cur.execute(f"""SELECT id FROM reminders""")
        if (obj == "chat_id"):
            res = cur.execute(f"""SELECT chat_id FROM reminders""")

        rows = res.fetchall()
        return [row[0] for row in rows]


db = DataBase(con, cur)

# To create table run THIS file!
