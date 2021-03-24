import discord
from discord import embeds

# Help_function is used only to make a generic help function for all cogs.
# To make it generic, we use a cogName, a cogDescription, a list of (command name, command description, command usage) entries 
# and optionally a custom color. By default we use "0x5DD5AE" as the color.
# To add a custom emoji per function on your cog, just send the function name with the emoji!
# For example:
# "connect" can be sent as ":microphone: connect"
# Or you can use a custom emoji ID instead of a unicode one.

# The function call happens on main.py, where it looks if its just a simple help command and sends the general help command
# or if it needs to call a specific help for a specific cog, and makes that call.
# generateHelpEmbed: Recieves the cogName, cogDescription and helpList, as optional we can use color to embed the help message 
async def generateHelpEmbed(ctx, cogName, cogDescription, helpList, embedColor=0x5DD5AE):
    print("[Utils.Help_function.GenerateHelpEmbed] Loading help embed")

    embed = discord.Embed(title="Help " + str(cogName), description=cogDescription, color=embedColor)

    # Sets the bot icon as embed image
    discord.File("./src/img/botIcon.png", filename="botIcon.png")
    embed.set_image(url="attachment://botIcon.png")

    for commandName, commandDescription, commandUsage  in helpList:
        embed.add_field(name=commandName, value=commandDescription + "\n" + commandUsage, inline=False)

    # Returns the final embed to the cog can print it
    await ctx.send(embed = embed)

# returnCustomEmojiList: Returns a list of cog names and custom emoji, to be sent on the generic help command
def returnCustomEmojiList():
    # This is the custom emoji list for our general .help command
    # If you want to add a custom emoji for your cog, add it here!
    # cog_name : unicode emoji /  custom discord emojis
    cogEmoji = {
        "admin":"🤖",
        "sounds": "🎶",
    }

    return cogEmoji