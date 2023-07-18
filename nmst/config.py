from configparser import ConfigParser
import os

class NmstConfigParser(ConfigParser):
    def __init__(self, filename, *args, **kwargs):
        ConfigParser.__init__(self, *args, **kwargs)
        self.filename = filename
        self.read()

    def read(self):
        # first check if file exists. otherwise, load example file
        if not os.path.exists(self.filename):
            examplename = self.filename + '.example'
            with open(examplename, 'r') as example_config:
                config_lines = example_config.readlines()
                # TODO: smarter handling of the warning comments
                with open(self.filename, 'w') as config_file:
                    config_file.writelines(config_lines[3:])
        ConfigParser.read(self, self.filename)

    def save(self):
        with open(self.filename, 'w') as config_file:
            self.write(config_file)

config = NmstConfigParser('config.toml')
