import sqlite3

from silent_wol import settings


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None) -> list:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def get_chat_id(update, context) -> int:
    """
    Retrieves the chat id from the messages info from the bot

    :param update:
    :param context:
    :return: the chat id
    """
    try:
        return update.message.chat_id
    except Exception:
        try:
            return update.effective_message.chat_id
        except Exception:
            return context.effective_message.chat_id


class StatusCodes(object):
    """ List of possible status codes for the bot """

    OK = 0
    MAC_ADDRESS_ALREADY_EXISTS = 1
    PROCESS_ERROR = 2
    MISSING_NAME = 3
    MISSING_MAC = 4
    MAC_ADDRESS_INVALID = 5


class RegisterDeviceStates(object):
    """ List of possible states during the registration of a new device """

    NAME = 0
    MAC = 1


class DBWrapper(object):
    """ Context manager to handle all DB-related operations """

    def __init__(self):
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.cur.close()
        self.conn.close()

    def connect(self, db_path: str = settings.DB_PATH):
        """
        Sets up the connection with the DB

        :param db_path: the path to the DB
        """
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def get_devices(self) -> dict:
        """
        Gets all the stored devices

        :return: a dictionary describing all the stored devices
        """
        self.cur.execute("SELECT id, name, mac FROM devices")
        return {item[1]: {
            'id': item[0],
            'name': item[1],
            'mac': item[2]
        } for item in self.cur.fetchall()}

    def get_device(self, name: str) -> dict or None:
        """
        Gets a specific device

        :param name: the name of the device to retrieve
        :return: the device if found, None otherwise
        """
        self.cur.execute(f"SELECT id, name, mac FROM devices WHERE name=\"{name}\"")
        res = self.cur.fetchall()
        if res:
            return res[0]
        return None

    def insert_device(self, name: str, mac: str) -> None:
        """
        Inserts a new device in the DB

        :param name: the name of the new device
        :param mac: the mac address of the new device
        """
        sql = f"INSERT INTO devices (name, mac) VALUES (?, ?)"
        self.cur.execute(sql, (name, mac))
        self.conn.commit()

    def update_device_by_name(self, name: str, newName: str, mac: str) -> None:
        """
        Updates the device identified by the name with the info provided

        :param name: the old name of the device
        :param newName: the new name for the device
        :param mac: the new mac address for the device
        """
        dev = self.get_device(name)
        if dev:
            return self.update_device(dev['id'], newName, mac)

    def update_device(self, row_id: int, name: str = None, mac: str = None) -> None:
        """
        Updates the specified device with the provided information

        :param row_id: the ID of the device to update
        :param name: the new name for the device
        :param mac: the new mac address for the device
        """
        if not name and not mac:
            return

        sql = "UPDATE devices SET "
        if name:
            sql += f" name={name} "
        if mac:
            sql += f" mac={mac} "
        sql += f" WHERE id={row_id}"
        self.cur.execute(sql)
        self.conn.commit()

    def remove_device_by_name(self, name: str) -> None:
        dev = self.get_device(name)
        if dev:
            return self.remove_device(dev['id'])

    def remove_device(self, row_id: int) -> None:
        """
        Removes the specified device

        :param row_id: the ID of the device to remove
        """
        sql = f"SELECT count(*) FROM devices WHERE id={row_id}"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        if res[0][0] != 1:
            return

        sql = f"DELETE FROM devices WHERE id={row_id}"
        self.cur.execute(sql)
        self.conn.commit()
