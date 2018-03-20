import requests
from .PokemonSpawn import PokemonSpawn
from .Raid import Raid
import json
import logging

logger = logging.getLogger('mybot')


class RESTClient:

    def __init__(self, api_url, api_token):
        self.api_url = api_url
        self.auth_header = {'Authorization': 'Token ' + api_token}

    def post_pokemon(self, pokemon: PokemonSpawn):
        post_data = json.dumps({
            'poke_nr': pokemon.number,
            'poke_lat': pokemon.latitude,
            'poke_lon': pokemon.longitude,
            "poke_iv": pokemon.iv,
            "poke_lvl": pokemon.lvl,
            "poke_despawn_time": pokemon.despawn_time
        })
        logger.info(post_data)
        return requests.post(self.api_url, json=post_data, headers=self.auth_header)

    def post_raid(self, raid: Raid):
        raise NotImplemented
