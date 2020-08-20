# config: token, botID, prefix

import discord, json, asyncio, random, os
from discord.ext import commands


config = json.load(open("config.json", 'r'))
token = os.environ.get("token")
bot = commands.Bot(command_prefix = config["prefix"], case_insensitive = True)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.name}.")


emotesToRoles = {
    # emoteName: roleName
    "DeadbyDaylight": "DbD",
    "LeagueofLegends": "LoL",
    "MovieNights": "MovieNights",
    "Valorant": "Valorant",
    "AYAYA": "AnimeNights"
}

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)

    if payload.message_id == 654298613287223307:
        if payload.emoji.name in emotesToRoles:
            role = discord.utils.get(user.guild.roles, name = emotesToRoles[payload.emoji.name])
            await user.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)

    if payload.message_id == 654298613287223307:
        if payload.emoji.name in emotesToRoles:
            role = discord.utils.get(user.guild.roles, name = emotesToRoles[payload.emoji.name])
            await user.remove_roles(role)


@bot.command(aliases = ["commands", 'c'])
async def commandList(ctx):
    message = """
**.hug {@user}** | `This command will hug the tagged person. If there is no tagged person the bot will hug you.`
**.uwu** | `This command will return the namiuwu emote.`
**.eightBall {question}** - *[Aliases: 8ball, 8b, 8, eb]* | `This command will return a random answer to a question.`
**.chance** | `This command will return the probability of something in percent.`
**.commands** - *[Alias: c]* | `This command will return a list of commands.`"""

    return await ctx.message.channel.send(message)


@bot.command(pass_context = True)
async def hug(ctx, user: discord.User = None):
    if user:
        return await ctx.message.channel.send(f"<@{ctx.message.author.id}> hugged <@{user.id}> <:lissie1Heart:654279399234863124>")
    else:
        return await ctx.message.channel.send(f"<@{config['botID']}> hugged <@{ctx.message.author.id}> <:lissie1Heart:654279399234863124>")
   

@bot.command()
async def uwu(ctx):
    return await ctx.message.channel.send("<:namiuwu:637388708387094540>")


@bot.command(aliases = ['8ball', '8b', '8', 'eb'])
async def eightBall(ctx, *args):
    answers = [
        "Hell no <:OMEGALUL:619160710789857281>",
        "The chances are slim",
        "Perhaps",
        "For sure",
        "ohhhhh damn, you got this fam",
        "You wish!"
    ]
    try:
        if args[0]:
            return await ctx.message.channel.send(random.choice(answers))
    except IndexError:
        return await ctx.message.channel.send("No question detected.")


@bot.command()
async def chance(ctx, *args):
    return await ctx.message.channel.send(f"I've calculated with my big AI brain that there is a {random.randint(0, 100)}% chance.")


bot.run(token)