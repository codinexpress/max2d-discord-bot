import os
from dotenv import load_dotenv

# Load environment variables from .env file
try:
    load_dotenv()
except FileNotFoundError:
    print("Warning: .env file not found. Make sure you have created a .env file with your bot token.")

import discord
from discord.ext import commands
from discord.ext.commands import AutoShardedBot
bot = AutoShardedBot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')
    # Load cogs on startup
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded cog: {filename[:-3]}")
            except Exception as e:
                print(f"Failed to load cog: {filename[:-3]}")
                print(f"Error: {e}")


@bot.tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello, world!")


@bot.tree.command(name="load", description="Load a cog")
@commands.is_owner()
async def load_cog(interaction: discord.Interaction, cog: str):
    """Loads a cog."""  
    try:
        bot.load_extension(f"cogs.{cog}")
    except Exception as e:
        await interaction.response.send_message(f"**`ERROR:`** {type(e).__name__} - {e}")
    else:
        await interaction.response.send_message("**`SUCCESS`**")


@bot.tree.command(name="unload", description="Unload a cog")
@commands.is_owner()
async def unload_cog(interaction: discord.Interaction, cog: str):
    """Unloads a cog."""
    try:
        bot.unload_extension(f"cogs.{cog}")
    except Exception as e:
        await interaction.response.send_message(f"**`ERROR:`** {type(e).__name__} - {e}")
    else:
        await interaction.response.send_message("**`SUCCESS`**")


@bot.tree.command(name="sync", description="Sync commands to current guild")
@commands.is_owner()
async def sync_current_guild(interaction: discord.Interaction):
    """Syncs the bot's commands to the current guild."""
    await interaction.response.defer()  # Defer the response to allow for longer processing time
    await bot.tree.sync(guild=interaction.guild)
    await interaction.followup.send("Synced commands to current guild.")


@bot.tree.command(name="sync_guild", description="Sync commands to a specific guild")
@commands.is_owner()
@discord.app_commands.describe(guild_id="The ID of the guild to sync to")
async def sync_to_guild(interaction: discord.Interaction, guild_id: str):
    """Syncs the bot's commands to a specific guild."""
    await interaction.response.defer()
    try:
        guild = bot.get_guild(int(guild_id))
        if guild is None:
            await interaction.followup.send("Guild not found.")
            return
        await bot.tree.sync(guild=guild)
        await interaction.followup.send(f"Synced commands to guild: {guild.name}")
    except ValueError:
        await interaction.followup.send("Invalid guild ID.")


@bot.tree.command(name="sync_global", description="Sync commands globally")
@commands.is_owner()
async def sync_global(interaction: discord.Interaction):
    """Syncs the bot's commands globally."""
    await interaction.response.defer()
    await bot.tree.sync() 
    await interaction.followup.send("Synced commands globally.")


if __name__ == "__main__":
    # Get the Discord bot token from the environment variable DISCORD_BOT_TOKEN.
    # You need to set this environment variable before running the bot.
    # You can set it in your terminal like this:
    # export DISCORD_BOT_TOKEN="your_bot_token"
    # Replace "your_bot_token" with your actual bot token.
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if token is None:
        print("DISCORD_BOT_TOKEN environment variable is not set.")
    bot_owner_id = os.environ.get("BOT_OWNER_ID")
    if bot_owner_id is None:
        print("BOT_OWNER_ID environment variable is not set.")


    bot.run(token)
