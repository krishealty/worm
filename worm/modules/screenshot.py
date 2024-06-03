import os

from worm.lib.module import Module


class WormModule(Module):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Category': "manage",
            'Name': "screenshot",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Take device screenshot.",
            'Usage': "screenshot <local_path>",
            'MinArgs': 1,
            'NeedsRoot': False
        })

    def run(self, argc, argv):
        self.print_process(f"Taking screenshot...")
        self.device.send_command("screencap /data/local/tmp/screenshot.png")

        self.device.download('/data/local/tmp/screenshot.png', argv[1])
        self.device.send_command("rm /data/local/tmp/screenshot.png")
