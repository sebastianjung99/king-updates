import discord
from discord.ext import tasks, commands
import os

import tools


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
                bot.load_extension(f'cogs.{filename[:-3]}')
                tools.logger.info(f'Loaded Module {filename}')

        print("loaded all cogs")                

    except Exception as e:
        tools.logger.exception(e)


if __name__ == "__main__":
    # get discord api token and run bot
    discord_token = tools.get_json("secrets.json")['DISCORD']['BOT_TOKEN']
    bot.run(discord_token)