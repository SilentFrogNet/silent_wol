import os
import sys

from wol.db import engine, session
from wol.db.utils import create_tables
from wol.db.models import Device


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
    if isinstance(context, int):
        return context
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
        self.engine = engine
        self.session = session

    def __enter__(self):
        create_tables()
        # self.conn = self.engine.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close_all()

    def get_devices(self) -> dict:
        """
        Gets all the stored devices

        :return: a dictionary describing all the stored devices
        """
        devices = self.session.query(Device).all()
        res = {d.name: {'id': d.id, 'name': d.name, 'mac': d.mac, 'net_name': d.net_name} for d in devices}
        return res

    def get_device(self, name: str) -> dict or None:
        """
        Gets a specific device

        :param name: the name of the device to retrieve
        :return: the device if found, None otherwise
        """
        device = self.session.query(Device).filter_by(name=name).one()
        return device

    def insert_device(self, name: str, mac: str, net_name: str = None) -> None:
        """
        Inserts a new device in the DB

        :param name: the name of the new device
        :param mac: the mac address of the new device
        :param net_name: the real network name of the device used for the commands
        """
        if not net_name:
            net_name = name

        dev = Device(name=name, mac=mac, net_name=net_name)
        self.session.add(dev)
        self.session.commit()

    def update_device_by_name(self, name: str, new_name: str = None, mac: str = None, net_name: str = None) -> None:
        """
        Updates the device identified by the name with the info provided

        :param name: the old name of the device
        :param new_name: the new name for the device
        :param mac: the new mac address for the device
        :param net_name: the new network name for the device
        """
        dev = self.get_device(name)
        if dev:
            return self.update_device(dev['id'], new_name, mac, net_name)

    def update_device(self, row_id: int, name: str = None, mac: str = None, net_name: str = None) -> None:
        """
        Updates the specified device with the provided information

        :param row_id: the ID of the device to update
        :param name: the new name for the device
        :param mac: the new mac address for the device
        :param net_name: the new network name for the device
        """
        if not name and not mac and not net_name:
            return

        dev = self.session.query(Device).filter_by(id=row_id).one()
        if dev:
            if name:
                dev.name = name
            if mac:
                dev.mac = mac
            if net_name:
                dev.net_name = net_name

            self.session.add(dev)
            self.session.commit()

    def remove_device_by_name(self, name: str) -> None:
        """
        Removes the device identified by the name

        :param name: the name of the device
        """
        dev = self.get_device(name)
        if dev:
            return self.remove_device(dev['id'])
        return None

    def remove_device(self, row_id: int) -> None:
        """
        Removes the specified device

        :param row_id: the ID of the device to remove
        """
        dev = self.session.query(Device).filter_by(id=row_id).one()
        self.session.delete(dev)
        self.session.commit()


def to_int(val, default=0):
    try:
        return int(val)
    except ValueError:
        return default


def get_project_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
