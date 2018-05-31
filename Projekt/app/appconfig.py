import configparser
import sys


CONFIG_FILE = 'main.conf'


# Read config file
config = configparser.ConfigParser()
try:
    config.read(CONFIG_FILE)
except OSError as e:
    sys.exit(e)