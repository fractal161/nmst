"""Boilerplate config handlilng."""

from configparser import ConfigParser
import os


class NmstConfigParser(ConfigParser):
    """Thin wrapper class for a parser that reads and writes to a single file.
    """

    def __init__(self, filename, *args, **kwargs):
        ConfigParser.__init__(self, *args, **kwargs)
        self.filename = filename
        self.read()

    def read(self):
        """Read the config associated with the filename. If the file does not
        exist, the function looks for an example config file and copies that.
        """
        # first check if file exists. otherwise, load example file
        if not os.path.exists(self.filename):
            examplename = self.filename + '.example'
            with open(examplename, 'r', encoding='utf-8') as example_config:
                config_lines = example_config.readlines()
                # TODO: smarter handling of the warning comments
                with open(self.filename, 'w', encoding='utf-8') as config_file:
                    config_file.writelines(config_lines[3:])
        ConfigParser.read(self, self.filename)

    def save(self):
        """Writes the current config state to the filename."""
        with open(self.filename, 'w', encoding='utf-8') as config_file:
            self.write(config_file)

config = NmstConfigParser('config.toml')
