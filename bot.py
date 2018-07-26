import discord
from discord.ext import commands

from config import help_message, token, life_time

"""
Some background:
The "ctx" parameter in each function represents 
a "context" object. This object allows discord
to know the context of when the command was used.
For example, if I use the command and I am in the 
general text channel, then the context parameter
holds that information, so the bot knows to 
respond in that general text channel.

As for the pass_context=True thing, for some reason
all of the examples had that, and I am still working
on *why* that is needed. Lmk if you have any questions.
"""

# needed for putting bot in and out of voice channel
current_voice = None

"""
this creates a command bot. A bit different from the bot
we made in the tutorial. This is a bot that is meant just
for commands, whereas, I think, the one in the tutorial 
is for conversations. Why this is useful is because we
can create command functions which imo look a lot cleaner
than the whole "if message.startswith('!')" stuff.

For example, look at the hello command, which is so much 
cleaner than the one in the tutorial. It's just one line,
yung pattis likes that.
"""
bot = commands.Bot(command_prefix='?', description = "test bot")

# Remove default help command, created our own 
bot.remove_command('help')

def get_help_page(ctx) -> str:
    """
    creates the help page and returns it
    Just a helper function I made
    """

    begin = bot.formatter.format_help_for(ctx, ctx.command)[0][:4]
    end = bot.formatter.format_help_for(ctx, ctx.command)[0][-4:]

    return (begin + help_message + end)

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

@bot.command(pass_context=True)
async def purge(ctx, *args):
    """
    Mass Delete Messages that have key prefixes

    For testing purposes
    """
    channel = ctx.message.channel
    check = lambda msg: msg.content == "" or msg.content[0] in ['!', '&', '?'] # prefixes for bots
    await ctx.bot.purge_from(channel, limit=1000, check=check)
    await ctx.bot.say("Messages have been purged", delete_after=life_time)


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

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_command_error(error, ctx):
    """
    For if a user says a wrong command, or
    an error occurs when a command is inputted.

    This gives them the help page
    """

    await bot.send_message(ctx.message.channel, 'oh my, here are the correct commands')
    await bot.send_message(ctx.message.channel, get_help_page(ctx))

if __name__ == '__main__':
	bot.run(token)
