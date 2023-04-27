import discord
from discord.ext import tasks, commands
import os
import logging, coloredlogs

import tools


FORMATTER = logging.Formatter(tools.LOG_FORMAT)

DISCORD_LOGGER = logging.getLogger("discord")
DISCORD_LOGGER.setLevel(logging.INFO)
logging.getLogger("discord.http").setLevel(logging.INFO)

DISCORD_HANDLER = logging.FileHandler("log.log")
DISCORD_HANDLER.setFormatter(FORMATTER)

DISCORD_STREAM_HANDLER = logging.StreamHandler()
DISCORD_STREAM_HANDLER.setLevel(logging.DEBUG)
DISCORD_STREAM_HANDLER.setFormatter(coloredlogs.ColoredFormatter(tools.LOG_FORMAT))

DISCORD_LOGGER.addHandler(DISCORD_HANDLER)
DISCORD_LOGGER.addHandler(DISCORD_STREAM_HANDLER)


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)


@bot.event
async def on_ready():
    # loop through files in /cogs and load every file that ends with .py (load all cogs)
    try:    
        currentdir = os.path.dirname(os.path.realpath(__file__)) + '\cogs'
        for filename in os.listdir(currentdir):
            if filename.endswith('.py'):
                # remove '.py' and load extension
                await bot.load_extension(f'cogs.{filename[:-3]}')
                tools.LOGGER.info(f'Loaded Module {filename}')

        tools.LOGGER.info("loaded all cogs")                

    except Exception as e:
        tools.LOGGER.exception(e)


if __name__ == "__main__":
    # get discord api token and run bot
    discord_token = tools.get_json("secrets.json")['DISCORD']['BOT_TOKEN']
    bot.run(discord_token, log_handler=None)