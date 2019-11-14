import random
import time

from mqtt.core.smqtt import SilentMQTT


def read_from_thermometer():
    return random.randrange(15, 25)


def main():
    broker = "broker.mqttdashboard.com"  # "silent_mqtt"
    port = 1883  # 1883

    with SilentMQTT(broker, port) as smqtt:
        for _ in range(10):
            temperature = read_from_thermometer()
            (rc, mid) = smqtt.publish("testtopic/4", str(temperature), qos=1)
            print(f"RC: {rc} - MID: {mid}")
            # time.sleep(0.5)


if __name__ == '__main__':
    main()
