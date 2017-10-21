import discord
from discord.ext import commands
import random

description = '''InsurgentBot coded by Steffbeard. For use in the Insurgency Gym.
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
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send('No, {0.subcommand_passed} is not cool, only FreeDoum is.'.format(ctx))

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

@bot.command()
async def pickmap(ctx):
    """Picks a random map from the map pool"""
    await ctx.send(random.choice(mapPool))

@bot.command()
async def callout(ctx, map):
    """Gives you a video to the callouts for the specific map. Use .callout (map name)"""
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


bot.run('MzcwMDEyNjU1MjAyNTk4OTEy.DMg5fQ.3Jzs2volpAGyNEwI8TQS-raiKpA')
