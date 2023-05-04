from discord.ext import tasks, commands

import tools
import updates


CHANNEL_ID = 1099438978693857340


class bot_loop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = self.bot.get_channel(CHANNEL_ID)

        # get config
        self.config = tools.get_json("config.json")

        # store channel name, a bool value to check if live message has already been sent and 
        # time when channel went live
        self.twitch_channels = [[channel_name, False, None] for channel_name in self.config['TWITCH']]

        # start main loop
        self.main_loop.start()

    
    async def check_twitch(self):
        """
        Checks if a twitch channel is live and sends a message to self.channel if live.
        """

        for channel in self.twitch_channels:
            streamer = channel[0]
            is_live, title, start = updates.get_twitch_status(streamer)

            # check if live and if live if live message has already been sent
            if is_live and not channel[1]:
                # set to True and send message
                channel[1] = True                
                tools.LOGGER.info(f"Sending live message for {streamer}.")
                await self.channel.send(f'{streamer} is live: \"{title}\"\nhttps://twitch.tv/{streamer}')

                # create database entry                
                mariadb_connection, cursor = tools.get_db_connection()
                sql_statement = "INSERT INTO twitch (channel_name, title, online) VALUES (%s, %s, %s)"
                values = (streamer, title, start)                
                tools.LOGGER.info(f"Creating datbase entry {sql_statement}." % values)
                cursor.execute(sql_statement, values)
                mariadb_connection.commit()
                mariadb_connection.close()


            # if not live anymore set status to false
            elif not is_live and channel[1]:
                channel[1] = False


    @tasks.loop(seconds=30.0)
    async def main_loop(self):
        tools.LOGGER.debug(f"Checking Twitch statuses.")
        await self.check_twitch()


async def setup(bot):  
    await bot.add_cog(bot_loop(bot))