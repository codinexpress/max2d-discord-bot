import pytest
import discord
from discord.ext import commands
from unittest.mock import AsyncMock, patch, MagicMock
import logging
import sys

# Assuming your bot code is in a file named 'bot.py'
# Replace 'bot.py' with the actual file name if different
# from bot.py import MyBot  # Replace MyBot with your bot class name

# Mock the bot owner ID and discord token
@pytest.fixture
def bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="/", intents=intents)
    bot.owner_id = 1234567890  # Replace with a mock owner ID
    bot.load_extension = AsyncMock()
    bot.unload_extension = AsyncMock()

    # Mock the logger
    bot.logger = logging.getLogger('discord')
    handler = logging.StreamHandler(sys.stdout)
    bot.logger.addHandler(handler)
    return bot


@pytest.fixture
def mock_context(bot):
    ctx = AsyncMock()
    ctx.bot = bot
    ctx.send = AsyncMock()
    ctx.author = AsyncMock(id=bot.owner_id)
    return ctx


@pytest.mark.asyncio
async def test_hello_command(bot, mock_context):
    # Add your /hello command to the bot
    @bot.command(name="hello")
    async def hello(ctx):
        await ctx.send("Hello!")
        
    await bot.process_commands(mock_context)
    mock_context.send.assert_called_once_with("Hello!")

@pytest.mark.asyncio
async def test_load_command(bot, mock_context):
    # Add your /load command to the bot
    @bot.command(name="load")
    async def load_cog(ctx, cog_name):
        try:
            await bot.load_extension(cog_name)
            await ctx.send(f"Loaded {cog_name}")
        except Exception as e:
            await ctx.send(f"Failed to load {cog_name}: {e}")
            
    mock_context.content = "/load some_cog"
    await bot.process_commands(mock_context)
    bot.load_extension.assert_called_once_with("some_cog")
    mock_context.send.assert_called_once_with("Loaded some_cog")

@pytest.mark.asyncio
async def test_unload_command(bot, mock_context):
    # Add your /unload command to the bot
    @bot.command(name="unload")
    async def unload_cog(ctx, cog_name):
        try:
            await bot.unload_extension(cog_name)
            await ctx.send(f"Unloaded {cog_name}")
        except Exception as e:
            await ctx.send(f"Failed to unload {cog_name}: {e}")
            
    mock_context.content = "/unload some_cog"
    await bot.process_commands(mock_context)
    bot.unload_extension.assert_called_once_with("some_cog")
    mock_context.send.assert_called_once_with("Unloaded some_cog")

@pytest.mark.asyncio
async def test_logging(bot, mock_context, capsys):
    bot.logger.info("This is a test log message.")

    captured = capsys.readouterr()
    assert "This is a test log message." in captured.out