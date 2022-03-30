# autor : G@b
# date : Jul 20

import discord
import requests
import levelsys
from pubg import *
from pprint import pprint
from random import randint
from datetime import datetime
from pymongo import MongoClient
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Cog

cogs = [levelsys]

bot = commands.Bot(command_prefix="!g ", description="Gabot !")

for i in range(len(cogs)):
	cogs[i].setup(bot)

global clash_channel_created
clash_channel_created = False


@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name="en serviiiiiiice (!g ...)"))
	print("Prêt !")

@bot.command()
async def bonjour(ctx):
	print("Bonjour !")
	await ctx.send("Bonjour !")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Erreur: Remplissez tous les arguments.")

@bot.command()
async def serverInfo(ctx):
	server = ctx.guild
	serverName = server.name
	nombreDeSalonsTextuels = len(server.text_channels)
	nombreDSalonsVocaux = len(server.voice_channels)
	nombreDePersonne = server.member_count

	embed = discord.Embed(title=f"Infos du serveur {serverName}",
						  description=f"Informations propres au serveur {serverName}.",
						  colour=discord.Colour.dark_blue())

	embed.add_field(name="Salons textuels", value=nombreDeSalonsTextuels, inline=True)
	embed.add_field(name="Salons vocaux", value=nombreDSalonsVocaux, inline=True)
	embed.add_field(name="Personnes présentes", value=nombreDePersonne, inline=True)

	await ctx.send(embed=embed)

@bot.event
async def on_member_update(before, after):
	log_channel = bot.get_channel(766349787548090379)
	if before.display_name != after.display_name:
		embed = discord.Embed(title="Mise à jour du membre",
							  description="Surnom changé",
							  colour=after.colour,
							  timestamp = datetime.utcnow())

		fields = [("Avant", before.display_name, False),
				  ("After", after.display_name, False)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await log_channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
	log_channel = bot.get_channel(766349787548090379)
	if not after.author.bot:
		if before.content != after.content:
			embed = discord.Embed(title="Message édité dans le channel *{0}*".format(before.channel),
								  colour=after.author.colour,
								  description = f"Message de {after.author.display_name} édité par {after.author.display_name}",
								  timestamp = datetime.utcnow())

			fields = [("Avant", before.content, False),
					  ("Après", after.content, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await log_channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
	log_channel = bot.get_channel(766349787548090379)
	mesage_id = message.id

	if not message.author.bot:

		embed = discord.Embed(title="Message supprimé dans le channel *{0}*".format(message.channel),
							  colour=message.author.colour,
							  description = f"Message de {message.author.display_name} supprimé par {message.author.display_name}",
							  timestamp = datetime.utcnow())

		fields = [("Message", message.content, False)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=True)

		embed.add_field(name="Message id", value=mesage_id, inline=True)

		await log_channel.send(embed=embed)

@bot.command()
async def say(ctx, *text):
	text = " ".join(text)
	await ctx.send(text)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, nombre: int):
	messages = await ctx.channel.history(limit=nombre+1).flatten()
	for message in messages:
		await message.delete()

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, *reason):
	reason = " ".join(reason)
	print(reason)
	await ctx.guild.kick(user, reason=reason)
	embed = discord.Embed(title="**Expulsion**", description=f"{user} a été expulsé(e) !")
	await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.User, *reason):
	reason = " ".join(reason)
	print(reason)
	await ctx.guild.ban(user, reason=reason)
	embed = discord.Embed(title="**Bannissement**", description=f"{user} a été banni(e) !", colour=discord.Colour.red())
	await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	print(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason=reason)
			embed = discord.Embed(title="**Débannissement**", description=f"{user} a été débanni(e) !", colour=discord.Colour.blue())
			await ctx.send(embed=embed)
			return
	await ctx.send(f"L'utilisateur **{user}** est introuvable.")

@bot.command()
@commands.has_permissions(manage_permissions=True)
async def giveRole(ctx,  user: discord.Member, nom_role):
	member = user
	role = discord.utils.get(member.guild.roles, name = nom_role)
	await discord.Member.add_roles(member, role)
	await ctx.send(f"{user} a obtenu(e) le rôle **{role}** !")

@bot.command()
@commands.has_permissions(manage_permissions=True)
async def removeRole(ctx,  user: discord.Member, nom_role, *reason):
	reason = " ".join(reason)
	member = user
	role = discord.utils.get(member.guild.roles, name = nom_role)
	await discord.Member.remove_roles(member, role)
	await ctx.send(f"Le rôle **{role}** de *{user}* a été supprimé pour la raison suivante : **{reason}**")

@bot.command()
async def lolStats(ctx, joueur):
	embed = discord.Embed(
		title = joueur,
		description = f"Stats de {joueur}",
		url=f"https://euw.op.gg/summoner/userName={joueur}",
		colour = discord.Colour.blue()
	)
	embed.set_footer(text=f"https://euw.op.gg/summoner/userName={joueur}")
	embed.set_image(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fopgg-static.akamaized.net%2Fimages%2Flogo%2F2015%2Freverse.rectangle.png&f=1&nofb=1")
	embed.set_author(name="League of Legends")
	await ctx.send(embed=embed)


@bot.command()
async def randomNumber(ctx, min: int, max: int):
	a = randint(min, max)
	await ctx.send("Nombre obtenu entre {0} et {1} : **{2}**".format(str(min), str(max), str(a)))

@bot.command()
async def dlYoutube(ctx, url):
	url = url.split(".")
	if url[1] == "youtube":
		url[1] = url[1] + "pp"
		url = ".".join(url)
		await ctx.send(f"Lien de téléchargement : **{url}**")
	else:
		await ctx.send("Lien invalide.")

@bot.command()
async def dlYtb(ctx, url):
	url = url.split(".")
	if url[1] == "youtube":
		url[1] = url[1] + "pp"
		url = ".".join(url)
		await ctx.send(f"Lien de téléchargement : **{url}**")
	else:
		await ctx.send("Lien invalide.")

@bot.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison."):
	mutedRole = await getMuteRole(ctx)
	await member.add_roles(mutedRole, reason=reason)
	await ctx.send(f"*{member.mention}* a été mute pour la raison suivante : **{reason}**")

@bot.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison."):
	mutedRole = await getMuteRole(ctx)
	await member.remove_roles(mutedRole, reason=reason)
	await ctx.send(f"*{member.mention}* a été demute pour la raison suivante : **{reason}**")

async def createMuteRole(ctx):
	mutedRole = await ctx.guild.create_role(name="mute",
											permissions = discord.Permissions(
												send_messages=False,
												speak = False))
	for channel in ctx.guild.channels:
		await channel.set_permissions(mutedRole, send_messages=False, speak=False)

	return mutedRole

async def getMuteRole(ctx):
	roles = ctx.guild.roles
	for role in roles:
		if role.name == "mute":
			return role
	return await createMuteRole(ctx)

@bot.command()
async def shortUrl(ctx, url):
	api_key = "f77dec4421c46717596eb5ada3be396f7b428"
	url = url
	api_url = f"https://cutt.ly/api/api.php?key={api_key}&short={url}"

	data = requests.get(api_url).json()["url"]
	if data["status"] == 7:

		shortened_url = data["shortLink"]
		await ctx.send(f"Short url: **{shortened_url}**")
	else:
		await ctx.send("Impossible de rétrecir cette url.", data)


@bot.command()
@commands.has_any_role(655132343157129241)
async def clash(ctx):
	global clash_channel_created
	name = '♠️ CLASH ♠️'

	if not clash_channel_created:
		guild = ctx.message.guild
		clash_channel_created = True
		clash_role = guild.get_role(655132343157129241)
		category = discord.utils.get(ctx.guild.categories, name="Jeux Vidéos")

		overwrites = {
			guild.default_role: discord.PermissionOverwrite(read_messages=False),
			guild.me: discord.PermissionOverwrite(read_messages=True),
			clash_role: discord.PermissionOverwrite(read_messages=True)
		}

		create_channel = await guild.create_text_channel(name, overwrites=overwrites, category=category)
		channel_clash = discord.utils.get(ctx.guild.channels, name="♠-clash-♠")
		channel_clash_id = channel_clash.id

		embed = discord.Embed(
			title="CLASH",
			description=f"Création du channel <#{channel_clash_id}>",
			colour=discord.Colour.blue(),
			timestamp=datetime.utcnow(),
		)
		await ctx.send(embed=embed)

	else:
		clash_channel_created = False
		channel_clash = discord.utils.get(ctx.guild.channels, name="♠-clash-♠")
		channel_clash_id = channel_clash.id

		await channel_clash.delete()

		embed = discord.Embed(
			title="CLASH",
			description=f"Fermeture du channel {name}",
			colour=discord.Colour.red(),
			timestamp=datetime.utcnow(),
		)
		await ctx.send(embed=embed)


@bot.command()
async def pubg(ctx, player):
	player_id = get_player_id(player)
	season_id = get_season_id()

	stats = get_player_rank_stats(player_id, season_id)

	rank = get_player_rank(player_id, season_id)

	embed = discord.Embed(
		title=player,
		description=f"Stats de {player}",
		url=f"https://pubg.op.gg/user/{player}",
		colour=discord.Colour.orange()
	)

	embed.set_image(
		url="https://logo-logos.com/wp-content/uploads/2018/03/pubg.png")
	embed.set_author(name="PUBG stats")


	embed.add_field(name="Victoires", value=stats["wins"], inline=True)
	embed.add_field(name="Défaites", value=stats["defeats"], inline=True)
	embed.add_field(name="Win rate", value=stats["win_ratio"], inline=True)

	embed.add_field(name="Kills", value=stats["kills"], inline=True)
	embed.add_field(name="Morts", value=stats["deaths"], inline=True)
	embed.add_field(name="kd/a", value=stats["kda"], inline=True)

	embed.add_field(name="Rank", value=rank, inline=True)
	embed.add_field(name="Meilleur classement", value=stats["best_rank_point"], inline=True)
	embed.add_field(name="Rank moyen", value=stats["avg_rank"], inline=True)

	await ctx.send(embed=embed)

bot.run("NzM0NDY1ODcwMTkyOTY3NzY5.XxSG7w.qrkvYDE5Fj46VaOk1RZt97l15Vo")