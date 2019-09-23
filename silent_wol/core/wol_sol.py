import os

os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

from wakeonlan import send_magic_packet
from silent_mqtt.core.smqtt import SilentMQTT


class WolSol(object):
    """ Performs WoL and SoL operations on the specified devices """

    def __init__(self):
        self.smqtt = SilentMQTT()

    def wol(self, *macs):
        to_wake_up = list(set(macs))
        send_magic_packet(*to_wake_up)

    def sol(self, *macs):
        to_sleep = list(set(macs))
        self.smqtt.send_sol_packet(*to_sleep)
