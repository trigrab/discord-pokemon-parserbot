import discord
from .Configuration import Configuration
from .MessageParser import MessageParser
from .REST_Client import RESTClient
import aiohttp
import json
import logging

logger = logging.getLogger('mybot')


class Bot(discord.Client):

    def __init__(self, config_file):
        super().__init__()
        self.config = Configuration(config_file)
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.message_parser = MessageParser(self.config.embeds_ignore)
        self.rest = RESTClient(self.config.rest_api_url, self.config.rest_api_token)

    async def on_ready(self):
        logger.info('Logged in as')
        logger.info(self.user.name)
        self.log_server_info()
        logger.info("Bot is ready.")
        logger.info('------')

    def run(self):
        super().run(self.config.token, bot=False)

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_resumed(self):
        logger.info('resumed...')

    async def on_message(self, message: discord.Message):
        logger.info('---------------------')
        # if message is direct message ignore
        if message.channel.is_private:
            return
        # if message is from the logged in user ignore
        if message.author == self.user:
            return
        # if message is in server we do not want to scan, ignore
        if message.channel.server.name not in self.config.servers:
            return

        if message.channel.name in self.config.pokemon_channels:
            pokemon = self.message_parser.parse_pokemon(message)
            logger.info(json.dumps(pokemon.as_dict()))
            logger.info('Posted: ' + self.rest.post_pokemon(pokemon))
        elif message.channel.name in self.config.raid_channels:
            raid = self.message_parser.parse_raid(message)
            logger.info(json.dumps(raid.as_dict()))
            # TODO self.rest.post_pokemon(raid)
        else:
            logger.info(message.channel.name)
            logger.info(message.author)
            logger.info(message.content)
            logger.info(message.embeds)

        logger.info('---------------------')

    def log_server_info(self):
        server_data = []
        for server_name in self.config.servers:
            channel: discord.Channel = self.get_server_by_name(server_name)
            if channel is not None:
                server: discord.Server = channel.server
                server_data.append({
                    'id': server.id,
                    'name': server.name,
                    'members': server.member_count
                })
        logger.info('You are searching in these servers: ' + json.dumps(server_data))

    def get_server_by_name(self, server_name):
        return discord.utils.find(lambda c: c.server.name == server_name,
                                  self.get_all_channels())
