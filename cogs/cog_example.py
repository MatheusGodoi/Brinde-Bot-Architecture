import discord
import os
import time
from discord.ext import commands
from discord.utils import get
import src.utils.help_function as helpFunction

# This Cog is just a template to create your own cog with your own functions, and add it into the bot!
# First, we need to create a cog class:

# CogExample Class, used with {description of the cog usage}
class CogExample(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Functions ###########################################################################################################################################################
    # Cogs methods, can be commands used on text chat, or just functios used only inside the cog, to run other commands
    # This one is used by other functions. We can see this by the absence of the "@commands.command()" tag.
    # doSomething: Function that {description of this function purpose and usage}
    async def doSomething(self, ctx):
        # A required pratice to make debugging easier is to log the function and cog of the print
        # This is done with the structure "[cogExample.doSomething]" on all console logs (prints)
        # The tag follows [{cogClassName}.{functionCalled}] to make finding the culprit cog and function easier
        print("[CogExample.doSomething] Here I do something!")
        print("""[CogExample.doSomething] The 'self' argument dont need to be specified when calling this function, 
        as you will call this with 'self.doSomething(...)', python will use self as a argument by default.
        'ctx' is a context argument, provided by discord. This contains the message content, author, channel that was sent, command name, time, etc.
        Basically everything about the message context.\n
        """)

    # Commands Methods ####################################################################################################################################################
    # This method is a command used by the bot. You can set the function name to be called (.example in this case)
    # and a list of aliases, to account for different names, misstypes, etc.
    # exampleCommand: Function that {description of this command purpose and usage}
    @commands.command(pass_context=True, name="example", aliases=["examlpe", "exmp", "ex", "exampleCommand"])
    async def exampleCommand(self, ctx):
        print("[CogExample.exampleCommand] Here I do another thing!")
        print("[CogExample.exampleCommand] And I can use another methods too!")
        await self.doSomething(ctx)
        print("""[CogExample.exampleCommand] This function is a discord command.
        We also use the "self.doSomething(ctx)" method here!
        We can use any amount of commands that we wish, just need to take care with the names and aliases.
        If multiple commands use the same name or alisases, the first command with it will be run
        everytime, so if various commands use the same "example" command name, the first one will
        run, no matter how hard you try.\n
        """)

    # cog_exampleHelpCommand: Help function to get all cog usages
    # Important to have the EXACT cog name as the start of the function, as well as the same sufix HelpCommand, so we can find this command later
    # This is why on the cog called "cog_example", the command is called "cog_exampleHelpCommand"
    # This function with this exact name is called on `main.py` everytime a user runs the .help <cog name> command
    @commands.command(pass_context=True)
    async def cog_exampleHelpCommand(self, ctx):
        print("[CogExample.cog_exampleHelpCommand] Generating embed")
        # If it is, we use the generic help function to generate a embed
        # First we generate all needed fields

        # Again, super needed to have exact name
        cogName = "cog_example"

        # A brief description of this cog reason to exist
        cogDescription = "Example functions and template for new cogs"

        # A custom color for the embed (if you wish, can be left empty)
        cogEmbed = 0x000000
        # List of commands from this cog
        # This list MUST follow the template (command_name, command_description, command_usage) to be parsed correctly
        # A good pratice for the command_usage is to show some (but not all) of the aliases of the command
        # If all aliases are for errors (for example, examlpe a alias for example command) they can be left off
        # Another good thing to do is add a emoji for the function, so its easier to find and adds a bit of characteristic to it
        # You can use unicode emojis or use a custom discord emoji there
        helpList = [
            ("📚 example", "Example command on the template cog.", "`.example` | `.exmp` | `.ex`"),
            ]

        # Finally, we call the helpFunction from utils to generate our embed message and send it in the end
        print("[CogExample.cog_exampleHelpCommand] Sending embed\n")
        await helpFunction.generateHelpEmbed(ctx, cogName, cogDescription, helpList, cogEmbed)
        return


# One observation that I want to make is that ALL cogs methods are ASYNCHRONOUS! This is because the discord API nature,
# to prevent the bot from being locked in a command, all methods are async so the bot can handle various requests for various
# different commands at the same time. Because of that, all bot methods needs to be called with the "await" keyword, as seen in line 37.

# Setup function for the cog
# This will be the same with all cogs, just swapping the cog name on "bot.add_cog({cogClassName}(bot)"
# This setup is the function called by the discord API to add the cog on the bot.
# The "CogExample(bot)" must be swapped to "{Cog Class Name}(bot)", that we defined on line 11 of this file, to add it properly.
def setup(bot):
    bot.add_cog(CogExample(bot))

# Unload function for the cog
# This will be the same with all cogs, just swapping the cog name on "bot.remove_cog({cogClassName}(bot)"
# This teardow is the function called by the discord API to remove a cog on the bot.
# The "CogExample(bot)" must be swapped to "{Cog Class Name}(bot)", that we defined on line 11 of this file, to remove it properly.
def teardown(bot):
    bot.remove_cog(CogExample(bot))