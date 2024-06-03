from worm.lib.module import Module


class WormModule(Module):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Category': "manage",
            'Name': "shell",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Execute shell command on device.",
            'Usage': "shell <command>",
            'MinArgs': 1,
            'NeedsRoot': False
        })

    def run(self, argc, argv):
        output = self.device.send_command(' '.join(argv[1:]))
        self.print_empty(output)
