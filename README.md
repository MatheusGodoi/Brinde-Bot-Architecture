# Brinde-Bot-Architecture

Modular architecture for discord bots.<br>
Allows for reloading, updating from a git repository, enabling and disabling cogs on the fly, and more.<br>

# Table of Contents
1. [Description](#description)
2. [Features](#features)
3. [Structure](#structure)
4. [Usage](#usage)
5. [Adding new Cogs](#adding-new-cogs)
6. [Updating](#updating)
7. [TO-DO](#to-do)
8. [References](#references)

# Description

This bot was made using Python 3.9, to fill our personal discord server.<br>
Due to the amount of computer science students on our server, we decide to make the bot modular, in a way that is easy to anyone add your own functions on the bot.<br>

# Features

The features of the bot are:
- Modular cogs;<br>
The bot structure allows for a very modular style, allowing for multiple cogs with different usages be created with ease
- Auto load cogs;<br>
Provided everything was configured, any user added cog will be loaded on startup
- Admin powers;<br>
Users with access can reload, load or unload cogs without needing to shutdown the bot. You can even get updates directly from git
- Generic imports;<br>
We want to make useful functions as generic as we can, to put it in our [utils](/src//utils/) folder, allowing multiple cogs to take advantage of that

Current cogs and functions:
- [CogExample](/cogs/cog_example.py): Template for new cogs<br>
ExampleCommand: Logs some messages on the terminal. Just as example!

- [Main](/cogs/main.py): Not a cog on itself, but the main bot code<br>
Ping: Pong!<br>
Echo: Makes the bot repeat something.<br>
Help: The main help function on the bot. Everytime a .help is called, its this one. If a cog name is passed with the command, the bot will look for the respective cog help command and invoke it instead.<br>

- [Admin](/cogs/admin.py): Admin related functions, mainly reloading cogs<br>
ReloadCogs: Tries to reload existent cogs, load new ones, deactivate the disabled cogs. Skips `git pull` as default, but can be run by passing 't' as argument with the command<br>
LoadCog: Tries to activate a cog and reload all cogs; Skips `git pull`;<br>
UnloadCog: Tries to deactivate a cog and reload all cogs; Skips `git pull`;<br>
ReadCogs: Reads teh entire cogfile and sends as text;<br>

Current utils:
- [Voice_Channel](/src/utils/voice_channel.py): Stores a "Connect" and "Disconnect" a voice channel function;<br> 
- [CogFile_Manage](/src/utils/cogfile_manage.py): Holds utils functions to read and write from the CogFile;<br> 
- [Help_Functipn](/src/utils/help_function.py): Generates a help embed message with given arguments, to make generic help functions easier;<br>

# Structure

This bot uses the following structure:
```
root
├ src
| └ utils
|   └ utils.py
├ cogs
| └ cogs.py
├ main.py
├ .env
├ .gitignore
├ cogFile.txt
└ README.md
```

The following architeture is as follow:
- **/**<br>
`cogFile.txt` TXT file that stores all cogs names. This file is read on startup to load all cogs on the bot;<br>
`main.py` Main module of the bot. Responsible for the startup and cog loading;<br>
`.env` Env file that is read to find a discord app token and a list of user id with admin acces for the AdminCog;<br>
- **/src/**<br> 
Folder for files used on the code. Can be used to store sound files, images, etc. By default we include:<br>
`utils` Folder that have utils generic functions, to be imported on other cogs; Stores a empty *\_\_init\_\_.py* due to the nature of python imports;<br>
- **/cogs/**<br>
Folder to store all the user made cogs for the bot. This folder is read and loaded on startup; Stores a empty *\_\_init\_\_.py* due to the nature of python imports;<br>

# Usage

To run the bot you need:
- Python 3.x
- PIP<br>
Can be downloaded with `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py` and then `python3 get-pip.py` or `python get-pip.py` on windows
- Discord python package<br>
Can be downloaded with `python3 -m pip install -U discord.py` or  `python -m pip install -U discord.py` on windows
- Dotenv python package<br>
Can be download with `python3 -m pip install -U python-dotenv` or `python -m pip install -U python-dotenv` on windows
- .env file on root folder
This file will hold your discord_token and admin_list credentials, in this structure:<br>
```
DISCORD_TOKEN=ABCdefGHIjklMNOpqrStUvWxYz123-gg
ADMIN_LIST={"101","202","303", "404"}
```
*For help with this .env file, check .env.example*

With everything set-up, run the main code `python main.py` on the root folder to execute the bot.<br>
It will turn on, load all cogs and be ready for usage on discord server.

# Adding new Cogs

To add a new cog, you need to:
* Create a new cog. This can be made is many ways, and is recommended to use the provided [cog_example.py](/cogs/cog_example.py) to create one;
* Place it on the `/cogs` folder. Its the folder used to store and load all cogs;
* After coding your own cog with your functions, add it to the [cogFile.txt](/cogFile.txt)<br>
This .txt is read on startup, and loads all cogs there. Remember to place the FILENAME of your cog, without the .py extension;
* Restart your bot. After the cogs where placed on the right folder and the name added on the txt file, you can restart the bot to make it reload all cogs, and test your commands;
* Merge your changes. If everything works, merge/open a pull request on the repository so everyone can update the changes and use the same BrindeBot version

# Updating

If you clone this bot into a git repository, and use one to add cogs/maintain the bot, you can use the [AdminCog](/cogs/admin.py) to pull changes directly from there, and reload.<br>
Doing so is easy: Just create a new git repository, place this architecture there, and everytime something is merged, you can run `.reload t` on the discord text channel<br>
to force the bot into doing `git pull` and loading all cogs on the cogFile.txt.<br>

## Reloading

If you have **admin rights** on the bot (not on discord server!) set by the *.env* file, you can use the [AdminCog](/cogs/admin.py) for specific functions.<br>
These are:
- `loadCog`: Activates a single cog on the cogFile (if its deactivated) and reloads;
- `unloadCog`: Deactivates a single cog on the cogFile (if its activated) and reloads;
- `reloadAll`: Reads the entire cogFile, loads/reloads all active cogs and unloads all deactives cogs; Can be set to run `git pull` before reloading by passing a 't' as argument with the command, ignores by default;

# TO-DO:
Future features planned for the bot<br>
```
Nothing planned... for now!
```

# References
Link references to building the bot and cogs
- https://discordpy.readthedocs.io/en/latest/index.html
- https://discordpy.readthedocs.io/en/latest/quickstart.html
- https://discordpy.readthedocs.io/en/latest/api.html
- https://discordpy.readthedocs.io/en/latest/ext/commands/extensions.html
- https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
- https://realpython.com/how-to-make-a-discord-bot-python/
