import discord
from discord.ext import commands, tasks
import asyncio
import os

from datetime import datetime, timedelta
import pytz
import calendar
from PIL import Image


file = open("token.txt", "r")
TOKEN = file.readline().strip()
file.close()

# Leaderboard widget URL
URL = 'https://unbelievaboat.com/leaderboard/479082443748671488/widget'
# Channel ID
channel_id = 678680878934786059

alarm_time = '20:00'

client = commands.Bot(command_prefix = '!')


def render_lb():
    os.system('chromium-browser --headless --disable-gpu --window-size=600,480 --default-background-color=0 --screenshot=/home/pi/leaderboard-bot/lb.png --virtual-time-budget=6000 ' + URL)
    
    im = Image.open(r'lb.png')
    im_c = im.crop((0, 0, 580, 480))
    im_c.save('lb_c.png')


@client.event
async def on_ready():
    time_check.start()
    print('Bot online')

@client.command()
async def echo(ctx, arg):
    await ctx.send(arg)

@client.command()
async def lb(ctx):
    render_lb()
    await ctx.send(file=discord.File('lb_c.png'))

@tasks.loop(minutes=1)
async def time_check():
    channel = client.get_channel(channel_id)
    now = datetime.now()
    fmt_time = datetime.strftime(now, '%H:%M')
    try:
        render_lb()
        if fmt_time == alarm_time:
            await channel.send(file=discord.File('lb_c.png'))
        elif calendar.monthrange(now.year, now.month)[1] == now.day and fmt_time == '23:00':
            await channel.send('@everyone FINAL RESULTS', file=discord.File('lb_c.png'))
    except Exception as ex:
        em = discord.Embed(title='Error', description=str(ex), colour=0xF44336)
        await channel.send(embed=em)


client.run(TOKEN)
