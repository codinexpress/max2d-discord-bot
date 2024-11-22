import discord
from discord.ext import commands
import logging
import logging.handlers
import os

# Configure logging
log_dir = 'resources/logging'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'discord.log')

handler = logging.handlers.RotatingFileHandler(
    log_file, maxBytes=10 * 1024 * 1024, backupCount=5
)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.DEBUG) 

class LoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__) 

    @commands.Cog.listener()
    async def on_message(self, message):
        self.logger.debug(f"{message.author}: {message.content}") 