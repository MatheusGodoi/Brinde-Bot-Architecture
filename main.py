import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import src.utils.cogfile_manage as cogManage

# Set bot command prefix
bot = commands.Bot(command_prefix='.')

# Loads the DISCORD_TOKEN as enviroment variables, from our .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# CornoBot Class
class CornoBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Events
# on_ready: Runs when the bot starts
@bot.event
async def on_ready():
    print("[CornoBot.on_ready] " + str(bot.user) + " connected!")
    await loadCogs()

# Utils functions
# loadCogs: Reads all cogs from a txt and tries to load them
async def loadCogs():
    print("[CornoBot.on_ready] Loading cogs...\n")

    cogList = cogManage.readCogFile()
    for cog in cogList:
        # Ignore deactivated cogs
        if cog[0] == "!":
            continue
        print("[CornoBot.on_ready] Loading " + cog)
        bot.load_extension("cogs." + cog)
    print("\n[CornoBot.on_ready] " + "All set!\n\n")

# Bot Run
bot.run(TOKEN)