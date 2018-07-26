import discord
from discord.ext import commands

token = 'NDcxOTYxNjU3ODgzNzU0NDk3.Djscfw.prkRhd_XrJZsM9pNVVNsIQAm7Mc'

"""
https://discordapp.com/api/oauth2/authorize?client_id=471961657883754497&permissions=0&scope=bot
"""

help_message = """

Test Bot!

A bot we can use for testing purposes.

!hello ->
	says hello

!purge ->
    Mass Delete Messages that have key prefixes.
    For testing purposes.
    Right now, it deletes all messages with '!' in it

!voice ->
    For joining/leaving the author's voice channel

    Simply joins and leaves the voice channel, for now
    Maybe we can use this to plays songs, potentially?

    Example:

    Me: !voice
    Bot: Joining Your Voice Channel

    Me: !voice
    Bot: Leaving Your Voice Channel

!help ->
	This message.

"""

current_voice = None

life_time = 10

bot = commands.Bot(command_prefix='!', description = "says hello")
# Remove default help command, created our own 
bot.remove_command('help')

@bot.command(pass_context = True)
async def help(ctx):
    await ctx.bot.say(get_help_page(ctx))

@bot.command(pass_context = True)
async def hello(ctx):
    """
    Says hello
    Me: !hello
    Bot: hello
    """
    await ctx.bot.say("hello")

@bot.event
async def on_command_error(error, ctx):
    """
    For if a user says a wrong command, or
    an error occurs when a command is inputted.

    This gives them the help page
    """

    await bot.send_message(ctx.message.channel, 'oh my, here are the correct commands')
    await bot.send_message(ctx.message.channel, get_help_page(ctx))


@bot.command(pass_context=True)
async def voice(ctx):
    """
    For joining/leaving the author's voice channel

    Simply joins and leaves the voice channel, for now.

    Obviously, you need to be in a voice channel first to
    use this command.
    
    Maybe we can use this to plays songs, potentially?

    Example:

    Me: !voice
    Bot: Joining Your Voice Channel

    Me: !voice
    Bot: Leaving Your Voice Channel

    """
    global current_voice
    
    server = ctx.message.server
    channel = ctx.message.author.voice_channel

    if ctx.bot.is_voice_connected(server):
        await ctx.bot.say("Leaving Your Voice Channel")
        for voice_client in ctx.bot.voice_clients:
            if (voice_client.server == ctx.message.server):
                return await voice_client.disconnect()
    else:
        current_voice = await ctx.bot.join_voice_channel(channel)
        await ctx.bot.say("Joining Your Voice Channel")

@bot.command(pass_context=True)
async def purge(ctx, *args):
    """
    Mass Delete Messages that have key prefixes

    For testing purposes
    """
    channel = ctx.message.channel
    check = lambda msg: msg.content == "" or msg.content[0] in ['!']
    await ctx.bot.purge_from(channel, limit=1000, check=check)
    await ctx.bot.say("Messages have been purged", delete_after=life_time)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

def get_help_page(ctx) -> str:
    """
    creates the help page and returns it
    """

    begin = bot.formatter.format_help_for(ctx, ctx.command)[0][:4]
    end = bot.formatter.format_help_for(ctx, ctx.command)[0][-4:]

    return (begin + help_message + end)

if __name__ == '__main__':
	bot.run(token)
