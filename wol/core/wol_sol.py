from wakeonlan import send_magic_packet

from mqtt.silent_events import SilentEvents
from wol.utils.custom_types import MacList


class WolSol(object):
    """ Performs WoL and SoL operations on the specified devices """

    def __init__(self):
        self.smqtt = SilentEvents("192.168.1.106")

    def wol(self, *macs: MacList) -> None:
        to_wake_up = list(set(macs))
        send_magic_packet(*to_wake_up)

    def sol(self, *macs: MacList) -> None:
        to_sleep = list(set(macs))
        self.smqtt.send_sol_packet(*to_sleep)
