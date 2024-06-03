import sys
import termios
import tty

from worm.lib.module import Module


class WormModule(Module):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Category': "manage",
            'Name': "keyboard",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Interact with device keyboard.",
            'Usage': "keyboard",
            'MinArgs': 0,
            'NeedsRoot': False
        })

    @staticmethod
    def get_char():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def run(self, argc, argv):
        self.print_process("Interacting with keyboard...")
        self.print_success("Interactive connection spawned!")

        self.print_information("Type text below.")
        while True:
            self.device.send_command(f"input text {self.get_char()}")
