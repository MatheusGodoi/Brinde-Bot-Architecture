import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import src.utils.cogfile_manage as cogManage
import src.utils.help_function as helpFunction

# Set bot command prefix
bot = commands.Bot(command_prefix='.')
bot.remove_command('help')


# Loads the DISCORD_TOKEN as enviroment variables, from our .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# BrindeBot Class
class BrindeBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Commands ############################################################################################################################################################
# echo: Simple function to debug. Makes the bot repeat a message
@bot.command(pass_context=True, name="echo")
async def echo(ctx, message="Send me something to echo 👺"):
    print("[BrindeBot.echo] Echoing " + message)
    await ctx.channel.send(message) 
    return

# ping: pong
@bot.command(pass_context=True, name="ping")
async def ping(ctx):
    print("[BrindeBot.ping] Ponging")
    await ctx.channel.send("Pong 🏓")
    return


# helpMessage: Default help message that shows all cogs and possible help functions
@bot.command(pass_context=True, name="help", aliases=["hlep"])
async def help(ctx, cogName=None):
    # First we check if we recieved a cog name on the command. If we did, we call the right cog help command
    if cogName != None:
        print("[BrindeBot.helpMessage] Calling right help command")
        if bot.get_command(cogName + "HelpCommand") != None:
            print("[BrindeBot.helpMessage] Sending cog embed help\n")
            await ctx.invoke(bot.get_command(cogName + "HelpCommand"))
            return
        else:
            print("[BrindeBot.helpMessage] Cog '" + cogName + "' help command not found\n")
            await ctx.channel.send("Cog `" + cogName + "` help function not found!")
            return

    print("[BrindeBot.helpMessage] Attempting to read all cogs")
    readCogs = cogManage.readCogFile()

    # Cleans the cog list everytime to prevent deactivated cogs from appearing
    cogList = []
    for cog in readCogs:
        # Ignore deactivated cogs
        if cog[0] == "!":
            continue
        # Ignore repetitions
        if cog not in cogList:
            cogList.append(cog)

    # Gets the emoji list
    cogEmoji = helpFunction.returnCustomEmojiList()

    print("[BrindeBot.helpMessage] Generating embed")

    embed = discord.Embed(title="Brinde Bot Help list", description="List of cogs that you can ask for more help", color=0x5DD5AE)
    for cog in cogList:
        if cog in cogEmoji:
            embed.add_field(name=cogEmoji[cog] + " " + cog, value=cog.title() + " functions and usage\n", inline=False)
        else:
            embed.add_field(name="⚙️" + " " + cog, value=cog.title() + " functions and usage\n", inline=False)

    # Sets the bot icon as a url to be embedded
    botIcon = discord.File("./src/img/botIcon.png", filename="botIcon.png")
    embed.set_thumbnail(url="attachment://botIcon.png")

    embed.set_footer(text="Do .help <cog name> to find out more!")

    print("[BrindeBot.helpMessage] Sending embed help\n")
    await ctx.channel.send(embed=embed, file=botIcon)


# Events ##############################################################################################################################################################
# on_ready: Runs when the bot starts
@bot.event
async def on_ready():
    print("[BrindeBot.on_ready] " + str(bot.user) + " connected!")
    await loadCogs()

# Functions ##########################################################################################################################################################
# loadCogs: Reads all cogs from a txt and tries to load them
async def loadCogs():
    print("[BrindeBot.on_ready] Loading cogs...\n")

    cogList = cogManage.readCogFile()
    for cog in cogList:
        # Ignore deactivated cogs
        if cog[0] == "!":
            continue
        print("[BrindeBot.on_ready] Loading " + cog)
        bot.load_extension("cogs." + cog)
    print("\n[BrindeBot.on_ready] " + "All set!\n\n")

# Bot Run
bot.run(TOKEN)