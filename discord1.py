import discord
import config
import asyncio
from discord.ext import commands
from asyncio import sleep

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_raw_reaction_add(payload):
    if config.postId == payload.message_id:
        member = payload.member
        guild = member.guild
        emoji = payload.emoji.name
        mainRole = None

        for role in guild.roles:
            role = discord.utils.find(lambda r: r.name == role.name, guild.roles)

            if role in member.roles:
                mainRole = role

        guilds = await(bot.fetch_guild(payload.guild_id))
        roles = discord.utils.get(guilds.roles, id=mainRole.id)
        member2 = await(guild.fetch_member(payload.user_id))

        if member is not None and str(mainRole) != "@everyone":
            await member2.remove_roles(roles)

        if emoji in config.roles.keys():
            role = discord.utils.get(guild.roles, id=config.roles[emoji])
            await member.add_roles(role)

@bot.command()
async def embed(ctx):
    embed = discord.Embed(title="**RULES FOR THIS SERVER**", description="__**In addition to the server rules, there are a license agreement and Discord rules.\nYou need to familiarize yourself with them so as not to be left without an account.**__\n[• DISCOVERYGUIDE](https://support.discord.com/hc/ru/articles/4409308485271-Discovery-Guidelines)\n[• TERMS](https://discord.com/terms)\n[• RULES](https://discord.com/guidelines)\n\n<:dot:1100744393637511260> **RULE1**\nIt is forbidden to advertise IN ANY FORM without the permission of the Server administration.\nThis also includes custom DM.\n\n<:dot:1100744393637511260> **RULE2**\nNo spam and no discussion in channels not intended for this purpose.\nIt is also forbidden to encourage others to spam.\n\n<:dot:1100744393637511260> **RULE3**\nNo inappropriate behavior. Begging, tagging, moderation and studio employees is prohibited. Insults (and in a comic form) Nazism, racism, humiliation of personalities, provocations, obscene expressions, etc. Unacceptable.\nAlways treat others with respect!\n\n<:dot:1100744393637511260> **RULE4**\nKeep personal fights away from the chat Insults in chat or in private messages are unacceptable no matter how you treat others.\n\n<:dot:1100744393637511260> **RULE5**\nNo Nsfw content or talk of illegal activity.\n\n<:dot:1100744393637511260> **RULE6**\nNo inappropriate or offensive usernames, statuses, profile descriptions or profile pictures.\nYou may be asked to change them.\n\n<:dot:1100744393637511260> **RULE7**\nYou may not impersonate other users, moderators, famous people or UNIQUAL employees.\n\n<:dot:1100744393637511260> **RULE8**\nMisinformation Cheating games for anything cheats and their distribution.\nBuying and selling something, distribution and similar events without the permission of the administration.\n\n<:dot:1100744393637511260> **RULE9**\nAvoid filters This applies to both words and links. If something is censored, it is censorship for a reason.\n\n<:dot:1100744393637511260> **RULE10**\nIt is forbidden to discuss politics and similar topics on this server. Guys be above all this, treat everyone with respect.\n\n<:dot:1100744393637511260> **RULE11**\n__**It is forbidden to intentionally interfere with communication in voice lobbies. Use a device or programs to change andor play other sounds.\nThe last word for the moderators: Listen and support the volunteers who keep this server running.**__", color=14929297)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member=None, time=None, *reason):
    server_members = ctx.guild.members 
    data = [m.roles for m in server_members if m.name == str(ctx.author)[0:str(ctx.author).index("#")]]
    value = False

    for i in data[0]:
        if str(i.name) in config.mainRoles:
            value = True

    if(member == ctx.author):
        await ctx.send("You can't muted yourself!")
    elif(value):
        guild = ctx.guild
        Reason = ""

        for i in reason:
            Reason += f" {i}"

        if not member:
            await ctx.send("You must mention a member to mute!")
        elif not time:
            await ctx.send("You must mention a time!")
        else:
            if Reason == "":
                Reason = "No reason given."

            server_members = ctx.guild.members
            data = [m.roles for m in server_members if m.name == str(member)[0:str(member).index("#")]]
            data2 = [m for m in server_members if m.name == str(member)[0:str(member).index("#")]]
            lst = list()
            embed1 = discord.Embed(title="NOT|IFICATION", description=f"You muted: on server\nTime: {time} seconds\nReason: {Reason}.", color=16122370)
            embed2 = discord.Embed(title="NOTIFICATION", description=f"You unmuted: on server\nTime: {time} seconds\nReason: {Reason}.", color=16122370)
            user = await bot.fetch_user(member.id)

            for i in data[0]:
                if i.name != "@everyone":
                    lst.append(i.id)
                    roles = discord.utils.get(guild.roles, id=i.id)
                    member2 = await(guild.fetch_member(member.id))
                    await member2.remove_roles(roles)

            Muted = discord.utils.get(guild.roles, name=config.mutedName)

            if not Muted:
                Muted = await guild.create_role(name=config.mutedName)

                for channel in guild.channels:
                    await channel.set_permissions(Muted, speak=False, send_messages=False, read_message_history=False, read_messages=False)

            await member.add_roles(Muted, reason=Reason)
            muted_embed = discord.Embed(title="NOTIFICATION SERVER", description=f"{member.mention} Was muted by {ctx.author.mention} for {Reason} to {time} seconds.")
            await user.send(embed=embed1)

            await ctx.send(embed=muted_embed)
            await asyncio.sleep(int(time))

            for i in lst:
                role = discord.utils.get(guild.roles, id=i)
                await member.add_roles(role)

            unmute_embed = discord.Embed(title="NOTIFICATION SERVER", description=f"Mute over! {ctx.author.mention} muted to {member.mention} for {Reason} is over after {time} seconds.")
            await ctx.send(embed=unmute_embed)
            await user.send(embed=embed2)

            for role in [r for r in ctx.guild.roles if r.id == Muted.id]:
                await role.delete()
    else:
        await ctx.send("You do not have sufficient rights to use this command!")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member):
    mutedRole = discord.utils.get(ctx.guild.roles, name=config.mutedName)

    unmute_embed = discord.Embed(title="NOTIFICATION SERVER", description=f"Mute over! {ctx.author} muted to {member} is over")
    embed2 = discord.Embed(title="NOTIFICATION", description=f"You unmuted: on server", color=16122370)
    user = await ctx.guild.fetch_member(int(str(member)[2:-1]))

    await user.remove_roles(mutedRole)
    await ctx.send(embed=unmute_embed)
    await user.send(embed=embed2)

@bot.command()
async def say(ctx, *text):
    v = ""

    for i in text:
        v += f" {i}"

    await ctx.send(v)

@bot.command()
async def ban(ctx, member=None, *reason):
    server_members = ctx.guild.members 
    data = [m.roles for m in server_members if m.name == str(ctx.author)[0:str(ctx.author).index("#")]]
    value = False
    id = int(str(member)[2:-1])
    member = ctx.guild.get_member(id)

    for i in data[0]:
        if str(i.name) in config.mainRoles:
            value = True

    if(member == ctx.author):
        await ctx.send("You can't banned yourself!")
    elif(value):
        Reason = ""

        for i in reason:
            Reason += f" {i}"

        if member == None or member == ctx.message.author:
            await ctx.channel.send("You cannot ban yourself")
            return

        if reason == None:
            Reason = "No reason given."

        message = discord.Embed(title="NOTIFICATION", description="You banned: on server\nTime: forever\nReason: {Reason}.", color=16122370)
        user = await bot.fetch_user(id)
        await user.send(embed=message)
        await ctx.guild.ban(member, reason=Reason)
    else:
        await ctx.send("You do not have sufficient rights to use this command!")

@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, member = None, *, reason = "No reason given."):
    if not member:
        await ctx.send("Enter ID user!")
    else:
        member = int(str(member)[2:-1])
        user = await bot.fetch_user(member)

        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f"The participant {user} was unbanned due to {reason}!")

bot.run(config.token)
