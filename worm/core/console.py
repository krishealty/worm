import cmd
import sys

from badges import Badges, Tables

from worm.core.device import Device


class Console(cmd.Cmd):
    """ Subclass of worm.core module.

    This subclass of worm.core modules is intended for providing
    main Worm Framework console interface.
    """

    def __init__(self) -> None:
        super().__init__()
        cmd.Cmd.__init__(self)

        self.badges = Badges()
        self.tables = Tables()

        self.devices = {}
        self.banner = """%clear%end

░██╗░░░░░░░██╗░█████╗░██████╗░███╗░░░███╗░░░
░██║░░██╗░░██║██╔══██╗██╔══██╗████╗░████║░░░
░╚██╗████╗██╔╝██║░░██║██████╔╝██╔████╔██║░░░
░░████╔═████║░██║░░██║██╔══██╗██║╚██╔╝██║░░░
░░╚██╔╝░╚██╔╝░╚█████╔╝██║░░██║██║░╚═╝░██║██╗
░░░╚═╝░░░╚═╝░░░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝

--=[ %bold%whiteWorm Framework 8.0.0%end
--=[ Maintained by Krish Lalwani (%linehttps://krish.l5.ca/%end)
"""

        self.prompt = '(worm)> '

    def do_help(self, _) -> None:
        """ Show available commands.

        :return None: None
        """

        self.tables.print_table("Core Commands", ('Command', 'Description'), *[
            ('clear', 'Clear terminal window.'),
            ('connect', 'Connect device.'),
            ('devices', 'Show connected devices.'),
            ('disconnect', 'Disconnect device.'),
            ('exit', 'Exit Ghost Framework.'),
            ('help', 'Show available commands.'),
            ('interact', 'Interact with device.')
        ])

    def do_exit(self, _) -> None:
        """ Exit worm Framework.

        :return None: None
        :raises EOFError: EOF error
        """

        for device in list(self.devices):
            self.devices[device]['device'].disconnect()
            del self.devices[device]

        raise EOFError

    def do_clear(self, _) -> None:
        """ Clear terminal window.

        :return None: None
        """

        self.badges.print_empty('%clear', end='')

    def do_connect(self, address: str) -> None:
        """ Connect device.

        :param str address: device host:port or just host
        :return None: None
        """

        if not address:
            self.badges.print_usage("connect <host>:[port]")
            return

        address = address.split(':')

        if len(address) < 2:
            host, port = address[0], 5555
        else:
            host, port = address[0], int(address[1])

        device = Device(host=host, port=port)

        if device.connect():
            self.devices.update({
                len(self.devices): {
                    'host': host,
                    'port': str(port),
                    'device': device
                }
            })
            self.badges.print_empty("")

            self.badges.print_information(
                f"Type %greendevices%end to list all connected devices.")
            self.badges.print_information(
                f"Type %greeninteract {str(len(self.devices) - 1)}%end "
                "to interact this device."
            )

    def do_devices(self, _) -> None:
        """ Show connected devices.

        :return None: None
        """

        if not self.devices:
            self.badges.print_warning("No devices connected.")
            return

        devices = []

        for device in self.devices:
            devices.append(
                (device, self.devices[device]['host'],
                 self.devices[device]['port']))

        self.tables.print_table("Connected Devices", ('ID', 'Host', 'Port'), *devices)

    def do_disconnect(self, device_id: int) -> None:
        """ Disconnect device.

        :param int device_id: device ID
        :return None: None
        """

        if not device_id:
            self.badges.print_usage("disconnect <id>")
            return

        device_id = int(device_id)

        if device_id not in self.devices:
            self.badges.print_error("Invalid device ID!")
            return

        self.devices[device_id]['device'].disconnect()
        self.devices.pop(device_id)

    def do_interact(self, device_id: int) -> None:
        """ Interact with device.

        :param int device_id: device ID
        """

        if not device_id:
            self.badges.print_usage("interact <id>")
            return

        device_id = int(device_id)

        if device_id not in self.devices:
            self.badges.print_error("Invalid device ID!")
            return

        self.badges.print_process(f"Interacting with device {str(device_id)}...")
        self.devices[device_id]['device'].interact()

    def do_EOF(self, _):
        """ Catch EOF.

        :return None: None
        :raises EOFError: EOF error
        """

        raise EOFError

    def default(self, line: str) -> None:
        """ Default unrecognized command handler.

        :param str line: line sent
        :return None: None
        """

        self.badges.print_error(f"Unrecognized command: {line.split()[0]}!")

    def emptyline(self) -> None:
        """ Do something on empty line.

        :return None: None
        """

        pass

    def shell(self) -> None:
        """ Run console shell.

        :return None: None
        """

        self.badges.print_empty(self.banner, translate=False)

        while True:
            try:
                cmd.Cmd.cmdloop(self)

            except (EOFError, KeyboardInterrupt):
                self.badges.print_empty(end='')
                break

            except Exception as e:
                self.badges.print_error("An error occurred: " + str(e) + "!")
