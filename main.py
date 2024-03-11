import discord
import random
import time
import asyncio
import schedule
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta, FR


from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound

intents = discord.Intents.all()
Münzwurf = 'Kopf', 'Zahl'
bot = commands.Bot(command_prefix=commands.when_mentioned_or("$"), intents = intents)
channel_id = 1138722823133737033

intents.messages = True
intents.guilds = True
intents.reactions = True
intents.members = True
intents.presences = True

last_reminder_friday = None
last_reminder_wednesday = None

@bot.event
async def on_ready():
    print(f"{bot.user} is Ready")
    await reminder_loop()

    bot.loop.create_task(activity())
    bot.loop.create_task(reminder_loop())


async def activity():
    while True:
        activity = discord.Activity(name="over " + str(len(bot.guilds)) + " server", type=discord.ActivityType.watching, status=discord.Status.online)
        await bot.change_presence(activity=discord.Game("Fachbereichseinsatz"), status=discord.Status.online)
        await asyncio.sleep(300)


async def reminder_loop():
    global last_reminder_friday, last_reminder_wednesday
    while True:
        current_datetime = datetime.now()
        today = datetime.date(current_datetime)

        #Freitag
        last_friday = today + relativedelta(day=31, weekday=FR(-1))
        if today == last_friday and current_datetime.hour == 12:
            if last_reminder_friday is None or (current_datetime - last_reminder_friday).days >= 1:
                await last_friday_of_month_reminder(channel_id)
                last_reminder_friday = current_datetime

        # Mittowoch
        if today.weekday() == 2 and today.isocalendar()[1] % 2 == 0 and current_datetime.hour == 12:
            if last_reminder_wednesday is None or (current_datetime - last_reminder_wednesday).days >= 14:
                await every_two_weeks_on_wednesday_reminder(channel_id)
                last_reminder_wednesday = current_datetime


        await asyncio.sleep(1)


async def every_two_weeks_on_wednesday_reminder(channel_id):
    channel = bot.get_channel(channel_id)
    await channel.send("Erinnerung am Mittwoch: Tragt Berufsschule ein und Pflegt euer ESS! @everyone")


async def last_friday_of_month_reminder(channel_id):
    channel = bot.get_channel(channel_id)
    await channel.send("Erinnerung am letzten Freitag: Tragt Berufsschule ein und Pflegt euer ESS! @everyone")
    await channel.send("Erinnerung am letzten Freitag: Das ist eure letzte chance für diesen Monat einzutragen!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Command not found")
    if isinstance(error, AttributeError):
        return


@bot.command(pass_context=True)
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("My latency is")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"My latency is `{int(ping)}ms`")
    print(f'Ping {int(ping)}ms')


@bot.command(pass_context=True)
async def schneeball(ctx):
    await ctx.send("Könnte ich Sie für Finanztipps Begeistern?")


bot.run(open("token.txt","r").readline())