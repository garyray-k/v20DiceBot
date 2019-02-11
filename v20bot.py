import discord
from discord.ext import commands
import random
import credentials


description = '''Vampire the Masquerade dice rolling bot.'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'Welcome {0.name} to {1.name}! Check out the test-channel or DM me `!help` for best ways to employ my services. Alternately, you can type `!help` and clutter up this channel as well.'.format(member, guild)
        await guild.system_channel.send(to_send)

@bot.event
async def on_command_error(ctx, args):
    await ctx.send("Command not found. Format is ` !r X Y ` or ` !s X Y `\nEnter ` !help ` for more help.")
    return

@bot.command(description="Rolls a dice pool")
async def r(ctx, diceCount:int, difficulty:int):
    """Rolls dice using the `!r X Y` format. X=Number of Dice. Y=Difficulty"""
    resultString = ''
    if (diceCount > 25):
        await ctx.send("You're no Antediluvian, %s." % ctx.message.author.name)
        return
    
    prefix = "Rolled %s for **%s** with difficulty %s. " % (diceCount, ctx.message.author.name, difficulty)

    resultString = calculateSuccess(False, diceCount, difficulty, ctx.message.author.name)
    await ctx.send(prefix + resultString)
    return

@bot.command(description="Rolls for Specialty")
async def s(ctx, diceCount:int, difficulty:int):
    """Rolls a Specialty roll. Successes are worth two. Uses the same `!s X Y` format."""
    resultString = ''
    if (diceCount > 25):
        await ctx.send("You're no Antediluvian, %s." % ctx.message.author.name)
        return
    
    prefix = "*Specialty* roll for **%s**, **%s** dice with difficulty **%s**. " % (ctx.message.author.name, diceCount, difficulty)

    resultString = calculateSuccess(True, diceCount, difficulty, ctx.message.author.name)
    await ctx.send(prefix + resultString)
    return

def calculateSuccess(isSepcialty:bool, dCount:int, diff:int, name:str):
    numberSuccesses = 0
    numberFailures = 0
    result = ''
    for r in range(0, dCount): 
            number = random.randint(1, 10)
            if (isSepcialty and (number == 10)):
                numberSuccesses += 2
            elif (number >= diff):
                numberSuccesses += 1
            
            if (number == 1):
                numberFailures += 1
            
            if (r == (dCount - 1)):
                result += str(number)
            else:
                result += str(number) + ', '
    
    resultFinal = "*(%s)* Successes: **%d**" % (result, (numberSuccesses - numberFailures))

    if(numberSuccesses > numberFailures):
        return "%s\n:white_check_mark: Success! Good job **%s**!" % (resultFinal, name)
    elif(numberFailures > numberSuccesses):
        return "%s\n:skull: Oh shit, **%s BOTCHED**!" % (resultFinal, name)
    elif(numberSuccesses == numberFailures):
        return "%s\n:x: **%s** failed!" % (resultFinal, name)

bot.run(credentials.token)