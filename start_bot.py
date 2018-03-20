from PokemonParser.Bot import Bot
import logging

logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
LOGGER1 = logging.getLogger('discord')
LOGGER2 = logging.getLogger('mybot')
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
LOGGER1.addHandler(consoleHandler)
LOGGER1.setLevel(level=logging.INFO)
LOGGER2.addHandler(consoleHandler)
LOGGER2.setLevel(level=logging.DEBUG)

bot = Bot('config.yml')
bot.run()
