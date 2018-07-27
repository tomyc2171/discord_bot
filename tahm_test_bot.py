'''
7.26.18 - Just a bunch of test commands for now. 
'''

import discord
from discord.ext import commands

BOT_PREFIX = ('&')
TOKEN = "NDcxNzkxNDgxNTMxNjYyMzM3.Djp-Dg.lpiiwhMJPo88kgUR450sCEJBJps"

bot = commands.Bot(command_prefix=BOT_PREFIX)

bot.remove_command('help')

@bot.command(pass_context=True)
async def help(ctx):
    help_message ='''
tahm test bot

tahm's testing bot.

&hello
    -Says hello.

&purge
    -Purges the following:
        -All commands (!, ?, &)
        -Any empty messages
        -Any text-formatted messages

&help
    -Shows this message.'''
    H = "```" + help_message + "```"
    await ctx.bot.say(H)

@bot.command(pass_context=True)
async def hello(ctx):
    await ctx.bot.say("hello")

@bot.command(pass_context=True)
async def purge(ctx):
    channel = ctx.message.channel
    check = lambda msg: msg.content == "" or msg.content[0] in ['!', '?', '&'] or msg.content[:3] == "```"

    await ctx.bot.purge_from(channel, limit=1000, check=check)    
    await ctx.bot.say("Purge Complete", delete_after=10)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')    

bot.run(TOKEN)
