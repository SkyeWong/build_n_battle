import os
import json 
import nextcord
from nextcord.ext import commands
from nextcord import Embed

TOKEN = os.environ["DISCORD_TOKEN"]

bot = commands.Bot(command_prefix="+", case_insensitive=True, activity=nextcord.Game(name="+help"), owner_ids={806334528230129695, 706126877668147272})
embed_colours = [0x0071ad, 0x0064a4, 0x007dbd, 0x0096d6, 0x19afef, 0x32c8ff]

def roundup(number, round_to):
    return number if number % round_to == 0 else number + round_to - number % round_to

def rounddown(number, round_to):
    return number if number % round_to == 0 else number - number % round_to
                
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    print("Connected servers/guilds:")
    for guild in bot.guilds:
        print(f"  -{guild.name}(id={guild.id})")    

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    if message.content.find(f"<@!{str(bot.user.id)}>") != -1:
        response = "Hello! I\"m SkyeBot, created by Skye Wong!"
        await message.channel.send(response)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.CheckFailure):
		await ctx.send("Only devs can use this command.\nOn the plus side, maybe this will be introduced to the game later!")
	elif isinstance(error, commands.CommandOnCooldown):
		cd_ui = Embed()
		cd_ui.title = "Woah, chill."
		cd_ui.description = f"Wait **{round(error.retry_after)}** seconds left before using it again."
		await ctx.send(embed=cd_ui)

for filename in os.listdir(f"cogs"):
    if filename.endswith("py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.load_extension("help_cogs.cog")

bot.run(TOKEN)
