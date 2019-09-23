import sqlite3

from silent_wol import settings


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def get_chat_id(update, context):
    try:
        return update.message.chat_id
    except Exception:
        try:
            return update.effective_message.chat_id
        except Exception:
            return context.effective_message.chat_id


class StatusCodes(object):
    OK = 0
    MAC_ADDRESS_ALREADY_EXISTS = 1
    PROCESS_ERROR = 2
    MISSING_NAME = 3
    MISSING_MAC = 4


class RegisterDevice(object):
    class States:
        NAME = 0
        MAC = 1


class DBWrapper(object):

    # TODO: move to context manager

    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self, db_path=settings.DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        return self.conn

    def get_devices(self):
        self.cur.execute("SELECT id, name, mac FROM devices")
        return {item[1]: {
            'id': item[0],
            'name': item[1],
            'mac': item[2]
        } for item in self.cur.fetchall()}

    def get_device(self, name):
        self.cur.execute(f"SELECT id, name, mac FROM devices WHERE name=\"{name}\"")
        return self.cur.fetchall()

    def insert_device(self, name, mac):
        sql = f"INSERT INTO devices (name, mac) VALUES (?, ?)"
        self.cur.execute(sql, (name, mac))

    def update_device(self, row_id, name=None, mac=None):
        if not name and not mac:
            return

        sql = "UPDATE devices SET "
        if name:
            sql += f" name={name} "
        if mac:
            sql += f" mac={mac} "
        sql += f" WHERE id={row_id}"
        self.cur.execute(sql)

    def remove_deice(self, row_id):
        sql = f"SELECT count(*) FROM devices WHERE id={row_id}"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        if res[0][0] != 1:
            return

        sql = f"DELETE FROM devices WHERE id={row_id}"
        self.cur.execute(sql)


db = DBWrapper()
