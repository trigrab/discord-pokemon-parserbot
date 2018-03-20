import logging
from yaml import safe_load

logger = logging.getLogger('mybot')


class Configuration(object):

    token = None
    servers = None
    pokemon_channels = None
    raid_channels = None
    embeds_ignore = None
    rest_api_url = None
    rest_api_token = None

    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            config = safe_load(file)
            for key in config:
                setattr(self, key, config[key])

