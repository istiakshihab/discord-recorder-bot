import discord
from discord.ext import commands, tasks
import ctypes
import ctypes.util
import logging

# Check and Load Opus Library

print("ctypes - Find opus:")
a = ctypes.util.find_library('opus')
print(a)
 
print("Discord - Load Opus:")
b = discord.opus.load_opus(a)
print(b)
 
print("Discord - Is loaded:")
c = discord.opus.is_loaded()
print(c)

# Set Command Prefix

bot = commands.Bot('>')

# Setup Logger

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Setup Wave File

number_txt_file = Path.cwd() / 'number.txt'
number_txt_file.touch(exist_ok=True)
number = int(number_txt_file.open('r').read() or 0)
waves_folder = (Path.cwd() / 'recordings')
waves_file_format = "recording{}.wav"
waves_folder.mkdir(parents=True, exist_ok=True)

# Setup >record Function

@bot.command()
async def record(ctx):
    global number
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
    wave_file = waves_folder / waves_file_format.format(number)
    wave_file.touch()
    fp = wave_file.open('rb')
    ctx.voice_client.listen(discord.WaveSink(str(wave_file)))
    await discord.utils.sleep_until(time.dt)
    ctx.voice_client.stop_listening()
    print(discord.File(fp, filename='record.wav'))
    await ctx.send("Recording being sent. Please wait!")
    await ctx.send('Here\'s, your record file.', file=discord.File(fp, filename=str(wave_file.name)))
    number += 1

# Setup >join Function

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

# Setup >leave Function

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

# Bot Client ID

bot.run('NzU2OTQ3OTY4MzQyNjIyMjI4.X2ZQuw.Wyzc6z0O6F6D-1U6GYh_309pM_Y')

