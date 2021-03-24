import asyncio
import discord
import importlib
import os
import re
import subprocess
import sys
import time
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import src.utils.cogfile_manage as cogManage


# Loads the ADMIN_LIST as enviroment variables, from our .env file on root folder
load_dotenv("../.env")
ADMIN_LIST = os.getenv('ADMIN_LIST').strip("\{\}").split(",")

# AdminCog Class, used with admin special functions. Used the env for adminList to see people with permission to run these commands
class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.adminList = ADMIN_LIST

    # Functions ###########################################################################################################################################################
    # runProcess: Used to run a terminal command
    async def runProcess(self, command):
        try:
            print("[AdminCog.runProcess] Git pull...")
            process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await process.communicate()
        except NotImplementedError:
            print("[AdminCog.runProcess] NotImplementedError")
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await self.bot.loop.run_in_executor(None, process.communicate)

        return [output.decode() for output in result]

    # reloadLoadExtension: Tries to reload cogs or load new ones
    def reloadLoadExtension(self, module):
        module = "cogs." + module
        try:
            self.bot.reload_extension(module)
            print("[AdminCog.reloadLoadExtension] Reloading " + str(module)) 
        except commands.ExtensionNotLoaded:
            print("[AdminCog.reloadLoadExtension] Loading " + str(module)) 
            self.bot.load_extension(module)

    # unloadExtension: Tries to deactivate cogs
    def unloadExtension(self, module):
        module = "cogs." + module
        try:
            self.bot.unload_extension(module)
            print("[AdminCog.unloadExtension] Unloading " + str(module)) 
        except commands.ExtensionNotLoaded:
            print("[AdminCog.unloadExtension] Cog " + str(module) + "not loaded") 

    # reloadAll: Tries to reload all cogs, pulling new ones from git.
    async def reloadAll(self, ctx, shouldPull):
        # Tries to run git pull in a process, to update the bot before reloading
        print("[AdminCog.reloadAll] Running process")

        # If it has a 't' as argument, it pulls, else it ignores the git pull step
        if shouldPull == "t":      
            async with ctx.typing():
                stdout, stderr = await self.runProcess('git pull')
                if stderr != "":
                    print("[AdminCog.reloadAll] stderr: " + str(stderr))

                # Progress and other stuff redirected to stderr in git pull
                # Messages like "fast forward" and files along with the text "already up-to-date" are in stdout
                # As we wish to rebuild even if git is up-to-date, we just print the result and keep the procces, without returning
                if stdout.startswith('Already up-to-date.'):
                    print("[AdminCog.reloadAll] Already up-to-date.")
                    # return
                else:
                    print("[AdminCog.reloadAll] Pulled changes")
        else:
            print("[AdminCog.reloadAll] Ignoring git pull")


        # One list to activate cogs, one list to deactive
        print("[AdminCog.reloadAll] Getting cog list")
        modulesActivate = []
        modulesDeactivate = []

        # Appends all files in cogFile.txt (We reload ALL cogs, even the ones that was not updated, and we unload deactive cogs)
        cogList = cogManage.readCogFile()
        for cog in cogList:
            # Ignore comments
            if cog[0] == "#":
                continue

            # Add cogs to be deactivated
            if cog[0] == "!":
                # Ignore repetitions
                if cog not in modulesDeactivate:
                    modulesDeactivate.append(cog[2:])
                continue

            # If it dont has a '!' on start, it is a cog to reload, and ignore repetitions
            if cog not in modulesActivate:
                modulesActivate.append(cog)

        print("[AdminCog.reloadAll] Starting reloads\n")
        # Tries to load/reload all cogs
        for module in modulesActivate:
            try:
                self.reloadLoadExtension(module)
            except commands.ExtensionError as e:
                print("[AdminCog.reloadAll] commands.ExtensionError " + str(e))

        print("[AdminCog.reloadAll] Starting unloads\n")
        # Tries to unload all cogs 
        for module in modulesDeactivate:
            try:
                self.unloadExtension(module)
            except commands.ExtensionError as e:
                print("[AdminCog.reloadAll] commands.ExtensionError " + str(e))

        print("[AdminCog.reloadAll] Finished rebuilding\n")

    # findPermission: Tries to read all the adminIDs from the env list, to see if the user has needed permissions
    async def findPermission(self, ctx):
        authorID = str(ctx.author.id)
        # Check the admin list
        for adminID in self.adminList:
            if adminID.strip("\"") == authorID:
                print("[AdminCog.findPermission] Accepted")
                return True
        print("[AdminCog.findPermission] Forbidden: authorID (" + str(authorID) + ") not found in adminList\n")
        for admin in ADMIN_LIST:
            print(admin)
        return False

    # Commands Methods ####################################################################################################################################################
    # reloadCogs: Attempts to reload all cogs of the bot, if the user has permission for that
    # Skipps git pull by default, can be activated by passin any argument with the command
    @commands.command(pass_context=True, name="reload", aliases=["rebuild", "restart"])
    async def reloadCogs(self, ctx, shouldPull="f"):
        print("[AdminCog.reloadCogs] Attempting to reload all cogs")
        userPermission = await self.findPermission(ctx)
        if userPermission:
            await self.reloadAll(ctx, shouldPull)

    # unloadCog: Attempts to deactivate a single cog, and then reloads all of them without git pull
    @commands.command(pass_context=True, name="unload", aliases=["unlaod", "deactivate"])
    async def unloadCog(self, ctx, cogName):
        print("[AdminCog.unloadCog] Attempting to unload " + cogName)
        userPermission = await self.findPermission(ctx)
        
        if userPermission:
            print("[AdminCog.unloadCog] Reading cogFile")
            cogList = cogManage.readCogFile()
            for index, cog in enumerate(cogList, start=0):
                # Ignore unloaded cogs
                if cog[0] == "!":
                    continue

                # Ignores the line terminator on cogFile
                if cog == cogName:
                    print("[AdminCog.unloadCog] Found cog to unload on line " + str(index+1))
                    cog = str("! " + cog)
                    cogList[index] = cog

                    # Clear the cogFile
                    await cogManage.clearCogFile()
                    # Calls the writer to make new cogFile
                    await cogManage.writeCogFile(cogList)

                    print("[AdminCog.unloadCog] Reloading cogs...\n")
                    # Reload all cogs to apply changes, ignoring git pull
                    await self.reloadCogs(ctx, "f")
                    return

            print("[AdminCog.unloadCog] Cog " + str(cogName) + " not found.\n")
        return

    # loadCog: Attempts to activate a single cog, and then reloads all of them without git pull
    @commands.command(pass_context=True, name="load", aliases=["laod", "activate"])
    async def loadCog(self, ctx, cogName):
        print("[AdminCog.loadCog] Attempting to load " + cogName)
        userPermission = await self.findPermission(ctx)
        
        if userPermission:
            print("[AdminCog.loadCog] Reading cogFile")
            cogList = cogManage.readCogFile()
            for index, cog in enumerate(cogList, start=0):
                # Ignores active cogs
                if cog[0] != "!":
                    continue

                # Ignores the line terminator on cogFile, looks for deactivated cogs
                if cog == ("! " + cogName):
                    print("[AdminCog.loadCog] Found cog to load on line " + str(index+1))
                    cog = str(cog.split("! ")[1])
                    cogList[index] = cog

                    # Clear the cogFile
                    await cogManage.clearCogFile()
                    # Calls the writer to make new cogFile
                    await cogManage.writeCogFile(cogList)

                    print("[AdminCog.loadCog] Reloading cogs...\n")
                    # Reload all cogs to apply changes, ignoring git pull
                    await self.reloadCogs(ctx, "f")
                    return

            print("[AdminCog.loadCog] Cog " + str(cogName) + " not found.\n")
        return

    # adminHelpCommand: Help function to get all cog usages
    @commands.command(pass_context=True)
    async def adminHelpCommand(self, ctx):
        print("[AdminCog.adminHelpCommand] Generating embed")
        # If it is, we use the generic help function to generate a embed
        # First we generate all needed fields
        cogName = "admin"
        cogDescription = "Admin tools to control bot cogs and updates"
        cogEmbed = 0xeb4034
        # List of commands from this cog
        helpList = [
            ("🔃 reload", "Reloads all cogs on the bot. Can do git pull if used with \"t\"", "`.reload` | `.rebuild` | `.reload t` | `.rebuild t`"),
            ("⬇️ load", "Activates and load a single cog.", "`.load <cog name>` | `.activate <cog name>`" ),
            ("⬆️ unload", "Deactivates and unloads a single cog." , "`.unload <cog name>` | `.deactivate <cog name>`"),
            ]

        print("[AdminCog.adminHelpCommand] Sending embed\n")
        await helpFunction.generateHelpEmbed(ctx, cogName, cogDescription, helpList, cogEmbed)
        return


# Setup function for the cog
def setup(bot):
    bot.add_cog(AdminCog(bot))

# Unload function for the cog
def teardown(bot):
    bot.remove_cog(AdminCog(bot))