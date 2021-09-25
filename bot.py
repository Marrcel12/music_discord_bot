from asyncio.tasks import sleep
import os, logging
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv
from yt_mp3 import yt_mp3
load_dotenv()
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)
description = "Bot"
bot_prefix = "!"

client = discord.Client()
bot = commands.Bot(command_prefix="$")
music_que = []
music_que_title = []


def list_of_channels(type):
    text_channel_list = []
    if type == "text":
        for guild in client.guilds:
            for channel in guild.text_channels:
                text_channel_list.append(channel.id)
    if type == "voice":
        for guild in client.guilds:
            for channel in guild.voice_channels:
                text_channel_list.append(channel.id) 
    return text_channel_list
# @bot.event
# async def on_ready():
#     print(f'{client.user} has connected to Discord!')
#     text_channels = list_of_channels("text")
#     text_channels = list_of_channels("voice")

# @bot.event
# async def on_message(message):
#     if "pong" in message.content:
#         await message.channel.send('ping')
    # if "graj" in message.content:
        

@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.author.voice.channel
    vc = await channel.connect()
@bot.command(pass_context=True)  
async def quit(ctx):
    for vc in bot.voice_clients:
        await vc.disconnect()

@bot.command(pass_context=True)  
async def graj(ctx,message):
    global music_que, music_que_title
    user=ctx.message.author
    voice_channel=ctx.message.author.voice.channel
    channel=None
    
    if voice_channel!= None:
        url = message
        try:
            ctx.vc = await voice_channel.connect()
        except:
            print("already connected ")
        try: 
            yt = yt_mp3(url)
            music_que.append(yt[0])
            music_que_title.append(yt[1])
            await discord.utils.get(ctx.guild.channels, name="orkabot").send("DJ ZBUKU dodał do kolejki, "+ url)   
            await discord.utils.get(ctx.guild.channels, name="orkabot").send("Pełna kolejka to: "+ " \n * ".join(music_que_title) )  

        except:
            print("something wrong with music append")
        if len(music_que) == 1:
            while len(music_que) > 0:
                print("GRAM")
                ctx.vc.play(discord.FFmpegPCMAudio(source=music_que[0]))
                # await discord.utils.get(ctx.guild.channels, name="orkabot").send("DJ ZBUKU gra, "+ url)   
                while ctx.vc.is_playing():
                    await asyncio.sleep(0.001)
                os.remove(music_que[0])
                music_que = music_que[1:] 
                music_que_title = music_que_title[1:]

                print("Song finished")             
    else:
        await client.say('User is not in a channel.')
@bot.command()  
async def pauza(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client                
    voice_channel.pause()
    await ctx.message.add_reaction('⏯')
@bot.command()  
async def wznow(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client                
    voice_channel.resume()
    await ctx.message.add_reaction('▶️')   
print("RUNNING.....")

bot.run(TOKEN)
