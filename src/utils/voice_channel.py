import discord
from discord.ext import commands
from discord.utils import get

# Voice_channel stores functions to join or leave a voice channel
# connect: Default function used by other cogs to join the voice channel
async def connect(botObj, ctx):
    if not ctx.message.author.voice:
        print("[Utils.Voice_channel.Connect] Not in a voice channel")
        botObj.response = "You are not connected to a voice channel"
        return

    channel = ctx.message.author.voice.channel
    voice = get(botObj.bot.voice_clients, guild=ctx.guild)

    print("[Utils.Voice_channel.Leave] Connecting to a voice channel")
    if voice and voice.is_connected():
        await voice.disconnect()
        voice = await channel.connect()
    else:
        voice = await channel.connect()

# disconnect: Default function used by other cogs to leave the voice channel
async def disconnect(botObj, ctx):
    voice = get(botObj.bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        print("[Utils.Voice_channel.Leave] Leaving voice channel")
        await voice.disconnect()
    else:
        print("[Utils.Voice_channel.Leave] Not in a voice channel")
        botObj.response = "Don't think I am in a voice channel"