from mqtt.silent_events import SilentEvents


def main():
    broker = "192.168.1.200"
    port = 1883

    se = SilentEvents(broker, port)

    # se.send_media_playpause({
    #     'domain': "workgroup",
    #     'name': "pc-ilo"
    # })
    se.send_mute({
        'domain': "workgroup",
        'name': "pc-ilo"
    },
    action="false")


if __name__ == '__main__':
    main()
