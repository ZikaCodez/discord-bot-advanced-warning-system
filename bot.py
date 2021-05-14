"""
TITLE : Warning system
AUTHOR : Scoopy#6969 (dc) | ScopesCodez (gh)
DESCRIPTION : Advanced warning system with a JSON database

Feel free to report any errors or issues!
"""

import discord  # import discord library
from discord.ext import commands  # import commands class from the discord package
import json  # import JSON library
import string  # import string library to use the string.digits method that returns a list of numbers
import random  # import random library to generate a random number

# you can change this, just make sure you've got member intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)  # defining our client


@bot.event
async def on_ready():
    # this will print "<your bot name> is online!" once your bot has started
    print(f"{bot.user} is online!")


# this is a function that will check if the guild exists in the JSON database
def check_if_guild_exists(guild_id: int):
    with open('warns.json', 'r') as f:
        load = json.load(f)

    try:
        load[str(guild_id)]
    except KeyError:
        load[str(guild_id)] = {}


# this is a function that will check if the user exists in the JSON database
def check_if_user_exists(guild_id: int, user_id: int):
    with open('warns.json', 'r') as f:
        load = json.load(f)

    try:
        load[str(guild_id)][str(user_id)]
    except KeyError:
        load[str(guild_id)][str(user_id)] = []


# this is a function that will add a warning to the user's warns
def add_warn(guild_id: int, user_id: int, staff_id: int, reason):
    with open('warns.json', 'r') as f:
        load = json.load(f)

    numbers = string.digits
    random_num = random.sample(numbers, 5)
    code = ''.join(random_num)

    jsonForm = {"warn": {"id": code, "reason": reason, "staffID": staff_id}}

    load[str(guild_id)][str(user_id)].append(jsonForm)

    with open('warns.json', 'w') as f:
        json.dump(load, f, indent=4)

    return code

# this function will return with all the user's warns


def get_user_warns(guild_id: int, user_id: int):
    with open('warns.json', 'r') as f:
        load = json.load(f)

    warnings = load[str(guild_id)][str(user_id)]

    return warnings

# this functions removes a warning from the user's warns


def remove_warn(guild_id: int, user_id: int, warn_id: int):
    with open('warns.json', 'r') as f:
        load = json.load(f)

    warnings = get_user_warns(guild_id, user_id)

    for x in warnings:
        if x['warn']['id'] == warn_id:
            jsonForm = {"warn": {
                "id": warn_id, "reason": x['warn']['reason'], "staffID": x['warn']['staffID']}}
            load[str(guild_id)][str(user_id)].remove(jsonForm)


@bot.command()
# this will make it required to have the "kick members" permissions to use the command
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    check_if_guild_exists(ctx.guild.id)
    check_if_user_exists(ctx.guild.id, member.id)
    code = add_warn(ctx.guild.id, member.id, ctx.author.id, reason)

    embed = discord.Embed(color=ctx.author.color,
                          title=f"Warning ID: {code}", description=f"✅ Warned **{member}** for : {reason}")
    await ctx.send(embed=embed)
    embed2 = discord.Embed(
        color=ctx.author.color, title=f"You have been warned in {ctx.guild.name}!", description=f"**Warning ID:** `{code}`\n**Reason:** {reason}")
    try:
        await member.send(embed=embed2)
    except:
        pass


@bot.command(aliases=['ws', 'warnings'])
# this will make it required to have "ban members" permissions to use the command
@commands.has_permissions(ban_members=True)
async def warns(ctx, member: discord.Member):
    check_if_guild_exists(ctx.guild.id)
    check_if_user_exists(ctx.guild.id, member.id)
    warns = get_user_warns(ctx.guild.id, member.id)

    if len(warns) == 0:
        embed = discord.Embed(color=member.color)
        embed.set_author(name=f"{member.name}'s warnings",
                         icon_url=member.avatar_url, description=f"**{member}** has no warning records.")
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(color=member.color)
    embed.set_author(name=f"{member.name}'s warnings",
                     icon_url=member.avatar_url)

    for x in warns:
        warn = x['warn']
        staff = bot.get_user(warn['staffID'])
        embed.add_field(
            name=f"ID: {warn['id']}", value=f"**Reason:** {warn['reason']}\n**Staff:** {staff} ({staff.id})", inline=False)

    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(kick_members=True)
async def unwarn(ctx, member: discord.Member, warn_id: int):
    check_if_guild_exists(ctx.guild.id)
    check_if_user_exists(ctx.guild.id, member.id)
    remove_warn(ctx.guild.id, member.id, warn_id)

    embed = discord.Embed(
        color=member.color, description=f"✅ Removed warning **{warn_id}** from **{member}**")


bot.run("your token here")
