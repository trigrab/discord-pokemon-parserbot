from discord.message import Message
import logging
from datetime import datetime
from datetime import date
from .PokemonSpawn import PokemonSpawn
from .Pokedex import Pokedex
from .Raid import Raid
from urllib.parse import urlparse
from urllib.parse import parse_qs

logger = logging.getLogger('mybot')


class MessageParser:
    """Parse message from discord channel to find pokemon and raids."""
    def __init__(self, embed_not_interesting):
        self.pokedex = Pokedex()
        self.pokedex.change_language('en')
        self.embed_not_interesting = embed_not_interesting

    def _extract_coordinates(self, url):
        """returns tuple(lat, lon) from google maps url"""
        query = parse_qs(urlparse(url).query)
        if 'q' not in query:
            return
        coord = query['q'][0].split(',')
        lat = coord[0]
        lon = coord[1]
        return lat, lon

    def parse_pokemon(self, message: Message):
        if message.content:
            logger.debug(message.content)
        if message.embeds:
            logger.debug(message.embeds)

        pokemon_data = PokemonSpawn()

        pokemon_data.number = self.pokedex.get_pokemon_id_by_name(message.author.name.split('#')[0])

        for embed in message.embeds:
            if isinstance(embed, dict):
                for key, value in embed.items():
                    if key == 'url':
                        lat, lon = self._extract_coordinates(value)
                        pokemon_data.latitude = lat
                        pokemon_data.longitude = lon
                    elif key == 'description':
                        try:
                            datestring = value[:8] + str(date.today())
                            pokemon_data.despawn_time = datetime.strptime(datestring,
                                                                          '%H:%M:%S%Y-%m-%d')
                        except ValueError:
                            logger.warning(str(key) + ': ' + str(value))
                    elif key == 'title':
                        v_list = value.split(' ')
                        for v in v_list:
                            s = v.split(':')
                            if len(s) > 1:
                                name = s[0]
                                value = s[1]
                                if name == "IV":
                                    value = value.replace('%', '')
                                    pokemon_data.iv = value
                                if name == "LV":
                                    pokemon_data.lvl = value
                    elif key not in self.embed_not_interesting:
                        logger.warning(str(key) + ': ' + str(value))
            else:
                logger.warning(embed)
        return pokemon_data

    def parse_raid(self, message: Message):
        if message.content:
            logger.debug(message.content)
        if message.embeds:
            logger.debug(message.embeds)
        return Raid()
