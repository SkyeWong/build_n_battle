import os
import nextcord
import random
from nextcord.ext import commands
from nextcord import Embed
import database as db

TOKEN = os.environ["DISCORD_TOKEN"]
DEVS_SERVER_ID = 919223073054539858

def get_prefix(bot, message): # define get_prefix
    sql = f"""
            SELECT prefix
            FROM server_prefixes
            WHERE server_id = {message.guild.id}
            """
    cursor = db.execute_query(sql)
    server_prefix = cursor.fetchall()[0][0]
    return server_prefix #recieve the prefix for the guild id given

bot = commands.Bot(command_prefix=(get_prefix), case_insensitive=True, activity=nextcord.Game(name="+help"), owner_ids={806334528230129695, 706126877668147272, 708141816020729867, 798720829583523861})
embed_colours = [
    # blues (deep -> light)
    0x00001B, 
    0x001034,
    0x00294D,
    0x194266,
    0x325B7F,
    # yellows (deep -> light)
    0xAA7300,
    0xC38C08,
    0xDCA521,
    0xF5BE3A,
    0xFFD753
    ]

def roundup(number, round_to):
    return number if number % round_to == 0 else number + round_to - number % round_to

def rounddown(number, round_to):
    return number if number % round_to == 0 else number - number % round_to

for filename in os.listdir(f"cogs"):
    if filename.endswith("py") and filename != "__init__.py":
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.load_extension("help_cogs.cog")
                    
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to nextcord!")
    print("Connected servers/guilds:")
    for guild in bot.guilds:
        print(f"  -{guild.name}(id={guild.id})")
        await guild.rollout_application_commands()
        sql = f"""
            SELECT prefix
            FROM server_prefixes
            WHERE server_id = {guild.id}
        """
        cursor = db.execute_query(sql)
        if cursor.fetchall() == []:
            sql = f"""
                INSERT INTO server_prefixes (server_id, prefix) VALUES ({guild.id}, "+")
            """
            db.execute_query(sql)
            db.conn.commit()

@bot.event
async def on_guild_join(guild):
    sql = f"""
        INSERT INTO server_prefixes (server_id, prefix) VALUES ({guild.id}, "+")
    """
    db.execute_query(sql)
    db.conn.commit()

@bot.event
async def on_guild_remove(guild):
    sql = f"""
        DELETE FROM server_prefixes WHERE server_id = "{guild.id}"
    """
    db.execute_query(sql)
    db.conn.commit()

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return

def cd_embed(ctx, error):
    cd_ui = Embed()
    cd_ui.title = "Woah, chill."
    cd_ui.description = f"Wait **{round(error.retry_after)}** seconds left before using `{ctx.clean_prefix}{ctx.command.qualified_name}` again."
    cd_ui.colour = random.choice(embed_colours)
    return cd_ui

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        if ctx.command.cog_name == "Dev Only":
            await ctx.send("Only devs can use this command.\nOn the plus side, maybe this will be introduced to the game later!")
        else:
            await ctx.send("You are missing the role(s)/permission(s) to use this command.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=cd_embed(ctx, error))
    else:
        raise error

@bot.event
async def on_application_command_error(interaction, error):
    if isinstance(error, commands.CommandOnCooldown):
        await interaction.response.send_message(embed=cd_embed(interaction, error))
    else:
        raise error

bot.run(TOKEN)
