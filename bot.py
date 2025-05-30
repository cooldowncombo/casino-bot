
import os
import discord
from discord.ext import commands
from utils.help import *
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True  # Add this line


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"Loaded extension {filename}")  # Add this line
            except Exception as e:
                print(f"Error loading extension {filename}: {e}")

@bot.event
async def on_connect():
    print("Bot connected to Discord.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("That command does not exist.")
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("You are missing a required argument.")
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.send("Invalid argument provided.")
    else:
        print(f"Error: {error}")
        await ctx.send("An error occurred while processing the command.")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
