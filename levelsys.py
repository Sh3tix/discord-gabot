import discord
from discord.ext import commands
from pymongo import MongoClient

bot_channel = 621739232154746882
talk_channel = [621739232154746882]

levelnum = [5, 10, 15]

cluster = MongoClient("mongodb+srv://gab:63W1FT6kJkYlUJtp@balthazar.emnlr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

levelling = cluster["discord"]["levelling"]

class levelsys(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.channel.id in talk_channel:
			stats = levelling.find_one({"id": message.author.id})
			if not message.author.bot:
				if stats is None:
					newUser = {"id": message.author.id, "xp": 100}
					levelling.insert_one(newUser)
				else:
					xp = stats["xp"] + 5
					levelling.update_one({"id": message.author.id}, {"$set":{"xp": xp}})
					lvl = 0
					while True:
						if xp < ((50*(lvl**2)) + (50*(lvl-1))):
							break
						lvl += 1
					xp -= ((50*((lvl-1)**2)) + (50*(lvl-1)))
					if xp == 0:
						await message.channel.send(f"Félicitation {message.author.mention} ! Tu es passé au niveau **{lvl - 1}**.")

	@commands.command()
	async def rank(self, ctx):
		if ctx.channel.id == bot_channel:
			stats = levelling.find_one({"id": ctx.author.id})
			if stats is None:
				embed = discord.Embed(description="Tu n'as aucun niveau !")
				await ctx.channel.send(embed=embed)
			else:
				xp = stats["xp"]
				lvl = 0
				rank = 0
				while True:
					if xp < ((50 * (lvl ** 2)) + (50 * lvl)):
						break
					lvl += 1
				xp -= ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))
				boxes = int((xp/(200*((1/2) * lvl))) * 20)
				rankings = levelling.find().sort("xp", -1)
				for x in rankings:
					rank += 1
					if stats["id"] == x["id"]:
						break

				embed = discord.Embed(title="Statisques de {}".format(ctx.author.name))
				embed.add_field(name="Nom", value=ctx.author.mention, inline=True)
				embed.add_field(name="XP", value=f"{xp}/{int(200*(1/2)*lvl)}", inline=True)
				embed.add_field(name="Niveau", value=f"{lvl - 1}", inline=True)
				embed.add_field(name="Rang", value=f"{rank}/{ctx.guild.member_count}", inline=True)
				embed.add_field(name="Progression", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=False)
				embed.set_thumbnail(url=ctx.author.avatar_url)
				await ctx.channel.send(embed=embed)

	@commands.command()
	async def leaderboard(self, ctx):
		if ctx.channel.id == bot_channel:
			rankings = levelling.find().sort("xp", -1)
			i = 1
			embed = discord.Embed(title="Rangs:")
			for x in rankings:
				try:
					temp = await self.client.fetch_user(x["id"])
					tempXP = x["xp"]
					embed.add_field(name=f"{i}: {temp.name}", value=f"XP total: {tempXP}", inline=False)
					i += 1
				except:
					pass
				if i == 11:
					break
			await ctx.channel.send(embed=embed)

def setup(client):
	client.add_cog(levelsys(client))
