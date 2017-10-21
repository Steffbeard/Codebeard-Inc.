import discord
from discord.ext import commands
import random
import time

description = '''InsurgentBot coded by Steffbeard and FreeDoum. For use in the Insurgency Gym.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='.', description=description)

@bot.event
async def on_ready():
    users = len(set(bot.get_all_members()))
    guilds = len(bot.guilds)
    game = discord.Game(name=".help | Coded by Steffbeard and FreeDoum.")
    await bot.change_presence(status=discord.Status.online, game=game)
    global mapPool
    global vote
    mapPool = ["District", "Embassy", "Market", "Uprising", "Station", "Verticality", "Heights", "Siege", "Ministry"]
    vote = False
    print("-----------------------------")
    print("Martydom is overrated")
    print("-----------------------------")
    print("Connected to {} guilds".format(guilds))
    print("-----------------------------")
    print("Currently serving {} users".format(users))
    print("-----------------------------")

@bot.command()
@commands.cooldown(1, .5, commands.BucketType.user)
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
@commands.cooldown(1, .5, commands.BucketType.user)
async def startvote(ctx):
    """Starts a vote for the map"""
    user = ctx.message.author
    channel = user.voice
    global mapVotes
    global voteID
    global mapPool
    global vote
    mapVotes = []
    voteID = []
    vote = True
    if channel is None:
        await ctx.send("You must be in a voice channel to do this command.")
    else:
        await ctx.send('```Please vote using .vote followed by the number associated with the map you desire the most\n\n1: District\n2: Embassy\n3: Market\n4: Uprising\n5: Station\n6: Verticality\n7: Heights\n8: Siege\n9: Ministry```')

@bot.command()
@commands.cooldown(1, .5, commands.BucketType.user)
async def vote(ctx, mapNum: int):
    """Registers vote"""
    user = ctx.message.author
    channel = user.voice
    global vote
    global vote
    if vote == False:
        await ctx.send('There is no ongoing vote')
        return
    global voteID
    if ctx.message.author in voteID:
        await ctx.send('You already voted smh')
        return
    global mapVotes
    global mapPool
    mapVotes.append(mapNum)
    voteID.append(ctx.message.author)
    mapName = mapPool[mapNum - 1]
    if channel is None:
        await ctx.send("You must be in a voice channel to do this command.")
    else:
        await ctx.send('Vote for {} registered'.format(mapName))

@bot.command()
@commands.cooldown(1, .5, commands.BucketType.user)
async def endvote(ctx):
    """Terminates the vote for the map"""
    user = ctx.message.author
    channel = user.voice
    global vote
    if vote == False:
        await ctx.send('There is no ongoing vote')
        return
    if channel is None:
        await ctx.send("You must be in a voice channel to do this command.")
        return
    global mapVotes
    global voteID
    global mapPool
    if mapVotes == []:
        await ctx.send('Vote ended, no vote registered')
    else:
        mapName = mapPool[random.choice(mapVotes) - 1]
        await ctx.send('Vote ended, the resulting map is {}'.format(mapName))
    mapVotes = 0
    voteID = 0
    vote = False

@bot.command(description='For when you wanna settle the score some other way')
@commands.cooldown(1, .5, commands.BucketType.user)
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.group()
@commands.cooldown(1, .5, commands.BucketType.user)
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool, only FreeDoum is.'.format(ctx))

@cool.command(name='bot')
@commands.cooldown(1, .5, commands.BucketType.user)
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

@bot.command()
@commands.cooldown(1, .5, commands.BucketType.user)
async def pickmap(ctx):
    """Picks a random map from the map pool"""
    await ctx.send(random.choice(mapPool))

@bot.command()
@commands.cooldown(1, .5, commands.BucketType.user)
async def callout(ctx, map):
    """Gives you a video to the callouts for the specific map."""
    map = map.lower()
    if map == "district":
        await ctx.send("Here you go: https://www.youtube.com/watch?v=LIUJM8guWrE&list=PL7a9PMAEeinpjMD0UXdlUy5hywhzHHjr8&index=4")
    elif map == "heights":
        await ctx.send("Here you are: https://www.youtube.com/watch?v=rH0pOM2w_xo")
    elif map == "market":
        await ctx.send("Here: https://www.youtube.com/watch?v=-B8VUUG8XQk&")
    elif map == "ministry":
        await ctx.send("Here you go: https://www.youtube.com/watch?v=_HCdrwFo8FU&")
    elif map == "station":
        await ctx.send("Here you are: https://www.youtube.com/watch?v=JEF2sG-KRIU")
    elif map == "siege":
        await ctx.send("Here: https://www.youtube.com/watch?v=JxmcAIU_lnY&list=PL7a9PMAEeinpjMD0UXdlUy5hywhzHHjr8&index=7")
    elif map == "uprising":
        await ctx.send("Here you go: https://www.youtube.com/watch?v=MUyQIhYA7-I")
    elif map == "embassy":
        await ctx.send("Here you are: https://www.youtube.com/watch?v=fmT18WHiPYM&index=5&list=PL7a9PMAEeinpjMD0UXdlUy5hywhzHHjr8")
    elif map == "verticality":
        await ctx.send("Here: https://www.youtube.com/watch?v=ITIfjU55SkI&index=10&list=PL7a9PMAEeinpjMD0UXdlUy5hywhzHHjr8")

@bot.command()
async def invite(ctx):
    """Gives an invite link for the bot."""
    await ctx.send("https://discordapp.com/oauth2/authorize?client_id=370012655202598912&scope=bot&permissions=1341643969")

@bot.command()
@commands.cooldown(1, .5, commands.BucketType.user)
async def info(ctx):
    """Provides info about the bot."""
    embed = discord.Embed(color=0x41454E, description="InsurgentBot by Steff and FreeDoum.")
    embed.title = "Info about InsurgentBot:"
    embed.add_field(name="What is InsurgentBot?", value="InsurgentBot is a Discord bot written in the discord.py library. It has many fun commands for users.", inline=False)
    embed.add_field(name="Who made this bot?", value="Coded by Steffbeard and FreeDoum, additional refrence by Mippy.", inline=False)
    embed.add_field(name="Credits to:", value="[Rapptz/discord.py](https://github.com/Rapptz/discord.py), [The users in the Discord API server](https://discord.gg/discord-api), [The Insurgency Gym](https://discord.gg/658eVDM), [Mippy](https://williamlomas.me)", inline=False)
    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def stats(ctx):
    """Shows InsurgentBot's stats."""
    servercount = len(bot.guilds)
    usercount = len(set(bot.get_all_members()))
    channelcount = len(set(bot.get_all_channels()))
    t1 = time.perf_counter()
    message = await ctx.send("Checking stats... :cd:")
    t2 = time.perf_counter()
    ping = round((t2-t1)*1000)
    embed = discord.Embed(color=0x41454E, description="Current Bot Stats")
    embed.title = "InsurgentBot Stats:"
    embed.add_field(name="Ping", value="{}ms".format(ping))
    embed.add_field(name="Servers", value=servercount)
    embed.add_field(name="Users", value=usercount)
    embed.add_field(name="Channels", value=channelcount)
    await message.delete()
    await ctx.send(embed=embed)

bot.run('MzcwMDEyNjU1MjAyNTk4OTEy.DMg5fQ.3Jzs2volpAGyNEwI8TQS-raiKpA')
