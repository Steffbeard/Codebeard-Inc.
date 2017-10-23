import random
import time
import discord
import csv
from discord.ext import commands

description = '''InsurgentBot coded by Steffbeard and FreeDoum. For use in the Insurgency Gym.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='.', description=description)


@bot.event
async def on_ready():
    users = len(set(bot.get_all_members()))
    guilds = len(bot.guilds)
    game = discord.Game(name=".help | homecoded by insurgents")
    await bot.change_presence(status=discord.Status.online, game=game)
    global mapPool #List of possible comp maps
    global vote #Indicates if a vote a vote is ongoing
    global coolPeople #List of people of cool people
    global mikeeQuotes #List of brilliant Mikee quotes
    mikeeQuotes = open('mikee.txt', 'r').readlines()
    mapPool = ["District", "Embassy", "Market", "Uprising", "Station", "Verticality", "Heights", "Siege", "Ministry"]
    vote = False
    coolPeople = ['<@178653059096772611>','<@267088096770785291>']
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
@commands.cooldown(1, 3, commands.BucketType.user)
async def mikee(ctx):
    """Enlightens you with some of Mikee's wisdom"""
    global mikeeQuotes
    random.seed()
    await ctx.send('***{}***'.format(random.choice(mikeeQuotes).rstrip('\n')))


@bot.command()
@commands.cooldown(1, .5, commands.BucketType.user)
async def startvote(ctx):
    """Starts a vote for the map"""
    user = ctx.message.author
    channel = user.voice
    global mapVotes
    global voteID #User ID of the voter
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
        random.seed()
        mapName = mapPool[mapVotes[random.randint(0,len(mapVotes) - 1)] - 1]
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
async def cool(ctx, member):
    """Says if a user is cool"""
    global coolPeople
    if str(member) in coolPeople:
        await ctx.send('{} is cool af bro'.format(member))
    else:
        await ctx.send('No, {} is not cool'.format(member))


@bot.command()
@commands.cooldown(1, .5, commands.BucketType.user)
async def pickmap(ctx):
    """Picks a random map from the map pool"""
    await ctx.send(random.choice(mapPool))


@bot.command()
@commands.cooldown(1, .5, commands.BucketType.user)
async def callouts(ctx, map):
    """Gives you a video to the callouts for the specific map."""
    map = map.lower()
    if map == "district":
        await ctx.send("Here you go: https://www.youtube.com/watch?v=LIUJM8guWrE&list=PL7a9PMAEeinpjMD0UXdlUy5hywhzHHjr8&index=4")
    elif map == "heights":
        await ctx.send("Here you are: https://www.youtube.com/watch?v=rH0pOM2w_xo")
    elif map == "market":
        await ctx.send("Here: https://www.youtube.com/watch?v=-B8VUUG8XQk&")
    elif map == "ministry":
        await ctx.send("Here you go: https://www.youtube.com/watch?v=1U9Nuzv1oXQ")
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
@commands.cooldown(1, .5, commands.BucketType.user)
async def info(ctx):
    """Provides info about the bot."""
    embed = discord.Embed(color=0x41454E, description="InsurgentBot by Steff and FreeDoum.")
    embed.title = "Info about InsurgentBot:"
    embed.add_field(name="What is InsurgentBot?",value="InsurgentBot is a Discord bot written in the discord.py library. It has many fun commands for users.",inline=False)
    embed.add_field(name="Who made this bot?", value="Coded by Steffbeard and FreeDoum, additional refrence by Mippy.",inline=False)
    embed.add_field(name="Credits to:",value="[Rapptz/discord.py](https://github.com/Rapptz/discord.py), [The users in the Discord API server](https://discord.gg/discord-api), [The Insurgency Gym](https://discord.gg/658eVDM), [Mippy](https://williamlomas.me)",inline=False)
    await ctx.send(embed=embed)


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def serverinfo(ctx):
    """Gives info about the server."""
    user = ctx.message.author
    guild = ctx.message.guild
    online = len([m.status for m in guild.members if m.status == discord.Status.online or m.status == discord.Status.idle])
    total_users = len(guild.members)
    passed = (ctx.message.created_at - guild.created_at).days
    created_at = ("Created {}. That's {} days ago!" "".format(guild.created_at.strftime("%d %b %Y %H:%M"),passed))
    categories = len(guild.categories)
    text = len(guild.text_channels)
    voice = len(guild.voice_channels)
    features = guild.features
    if features == []:
        features = "No VIP Features"
    else:
        features = guild.features
    data = discord.Embed(description=created_at, color=0x41454E)
    data.add_field(name="Region", value=str(guild.region))
    data.add_field(name="Features", value=features)
    data.add_field(name="Users", value="{}/{}".format(online, total_users))
    data.add_field(name="Roles", value=len(guild.roles))
    data.add_field(name="Channels", value="{} Categories | {} Text | {} Voice".format(categories, text, voice))
    data.add_field(name="Owner", value=str(guild.owner.mention))
    data.set_footer(text="Guild ID: {}".format(guild.id))
    if guild.icon_url:
        data.set_author(name=guild.name, url=guild.icon_url)
        data.set_thumbnail(url=guild.icon_url)
    else:
        data.set_author(name=guild.name)
    try:
        await ctx.send(embed=data)
    except discord.HTTPException:
        await ctx.send("{}, I need the `Embed Links` permission to send this command's output. :no_entry:".format(user.mention))


@bot.command()
@commands.cooldown(1, 1800)
async def here(ctx, int):
    """Asks @here to join PUG."""
    await ctx.send("@here Need {} more members for a :fire: PUG!".format(int))


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
    await message.delete()
    ping = round((t2 - t1) * 1000)
    embed = discord.Embed(color=0x41454E, description="Current Bot Stats")
    embed.title = "InsurgentBot Stats:"
    embed.add_field(name="Ping", value="{}ms".format(ping))
    embed.add_field(name="Servers", value=servercount)
    embed.add_field(name="Users", value=usercount)
    embed.add_field(name="Channels", value=channelcount)
    await ctx.send(embed=embed)  


@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def ping(ctx):
    """Pong!"""
    await ctx.send(":ping_pong: Pong!")

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def shrug(ctx):
    """¯\_(ツ)_/¯"""
    await ctx.send("¯\_(ツ)_/¯")

# COMMAND ERROR HANDLERS #####################################################################################################################################################################################

@info.error
async def info_error_handler(ctx, error):
    user = ctx.message.author
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("{}, you are being ratelimited. :no_entry:\nThis request has been logged, check `{}ratelimits` for more info.".format(user.mention, ctx.prefix))
        print("User {}({}) ratelimited at command 'info'".format(user, user.id))


@stats.error
async def stats_error_handler(ctx, error):
    user = ctx.message.author
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("{}, you are being ratelimited. :no_entry:\nThis request has been logged, check `{}ratelimits` for more info.".format(user.mention, ctx.prefix))
        print("User {}({}) ratelimited at command 'stats'".format(user, user.id))


@here.error
async def say_error_handler(ctx, error):
    user = ctx.message.author
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("{}, you are being ratelimited. :no_entry:".format(user.mention, ctx.prefix))
        print("User {}({}) ratelimited at command 'say'".format(user.name, user.id))
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("{}, you do not have the required permissions for this command. :no_entry:".format(user.mention))
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0x41454E, description="Command Help")
        embed.title = "{}here Help".format(ctx.prefix)
        embed.add_field(name="{}here <message>".format(ctx.prefix), value="Put a number of people needed to join the PUG!", inline=False)
        await ctx.send(embed=embed)


@add.error
async def say_error_handler(ctx, error):
    user = ctx.message.author
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("{}, you are being ratelimited. :no_entry:".format(user.mention, ctx.prefix))
        print("User {}({}) ratelimited at command 'add'".format(user.name, user.id))
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("{}, you do not have the required permissions for this command. :no_entry:".format(user.mention))

@ping.error
async def say_error_handler(ctx, error):
    user = ctx.message.author
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("{}, you are being ratelimited. :no_entry:".format(user.mention, ctx.prefix))
        print("User {}({}) ratelimited at command 'ping'".format(user.name, user.id))
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("{}, you do not have the required permissions for this command. :no_entry:".format(user.mention))

@shrug.error
async def say_error_handler(ctx, error):
    user = ctx.message.author
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("{}, you are being ratelimited. :no_entry:".format(user.mention, ctx.prefix))
        print("User {}({}) ratelimited at command 'shrug'".format(user.name, user.id))
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("{}, you do not have the required permissions for this command. :no_entry:".format(user.mention))
        
# RUN BOT #####################################################################################################################################################################################

bot.run('MzcwMDEyNjU1MjAyNTk4OTEy.DMg5fQ.3Jzs2volpAGyNEwI8TQS-raiKpA')
