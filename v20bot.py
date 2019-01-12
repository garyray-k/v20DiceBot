import discord
from discord.ext import commands
import random
import credentials

description = '''Vampire the Masquerade dice rolling bot.'''
bot = commands.Bot(command_prefix='!', description=description)
successValue = 1

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# @bot.event
# async def on_command_error(ctx, ):
#     await ctx.send("Please use format `!r X Y` where X=NumberOfDice and Y=DifficultyOfRoll")

@bot.event
async def on_member_join(self, member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)

@bot.event
async def on_command_error(ctx, args):
    await ctx.send("Command not found. Format is ` !r X Y ` or ` !s X Y `\nEnter ` !help ` for more help.")
    return

@bot.command(description="Rolls a dice pool")
async def r(ctx, diceCount:int, difficulty:int):
    """Rolls dice using the `!r X Y` format. X=Number of Dice. Y=Difficulty"""
    resultString = ''
    if (diceCount > 30):
        await ctx.send("You're no Antediluvian, %s." % ctx.message.author.name)
        return
    
    prefix = "Rolled %s for **%s** with difficulty %s. " % (diceCount, ctx.message.author.name, difficulty)

    resultString = calculateSuccess(1, diceCount, difficulty, ctx.message.author.name)
    await ctx.send(prefix + resultString)
    return

@bot.command(description="Rolls for Specialty")
async def s(ctx, diceCount:int, difficulty:int):
    """Rolls a Specialty roll. Successes are worth two. Uses the same `!s X Y` format."""
    resultString = ''
    if (diceCount > 30):
        await ctx.send("You're no Antediluvian, %s." % ctx.message.author.name)
        return
    
    prefix = "**Specialty** roll for **%s**, %s dice with difficulty %s. " % (ctx.message.author.name, diceCount, difficulty)

    resultString = calculateSuccess(2, diceCount, difficulty, ctx.message.author.name)
    await ctx.send(prefix + resultString)
    return

def calculateSuccess(successValue:int, dCount:int, diff:int, name:str):
    numberSuccesses = 0
    numberFailures = 0
    result = ''
    for r in range(0, dCount): 
            number = random.randint(1, 10)
            if (number >= diff):
                numberSuccesses += successValue
            
            if (number == 1):
                numberFailures += 1
            
            if (r == (dCount - 1)):
                result += str(number)
            else:
                result += str(number) + ', '

    if(numberSuccesses > numberFailures):
        return "(%s) Successes: %d Failures: %d \n:white_check_mark: Success! Good job %s!" % (result, numberSuccesses, numberFailures, name)
    elif(numberFailures > numberSuccesses):
        return "(%s) Successes: %d Failures: %d \n:skull: Oh shit, %s **BOTCHED**!" % (result, numberSuccesses, numberFailures, name)
    elif(numberSuccesses == numberFailures):
        return "(%s) Successes: %d Failures: %d \n:x: %s failed!" % (result, numberSuccesses, numberFailures, name)

bot.run(credentials.token)