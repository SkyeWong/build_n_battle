import os
import nextcord
import random
from nextcord.ext import commands
from nextcord import Embed, Interaction
import database as db

TOKEN = os.environ["DISCORD_TOKEN"]
DEVS_SERVER_ID = 919223073054539858

def get_prefix(bot, message): # define get_prefix
    if message.guild:
        sql = f"""
                SELECT prefix
                FROM server_prefixes
                WHERE server_id = {message.guild.id}
            """
        cursor = db.execute_query(sql)
        server_prefix = cursor.fetchall()[0][0]
        return server_prefix #recieve the prefix for the guild id given
    else:
        return "+"

bot = commands.Bot(command_prefix=(get_prefix), case_insensitive=True, activity=nextcord.Game(name="+help"), owner_ids={806334528230129695, 706126877668147272, 708141816020729867, 798720829583523861, 823522605352484916})
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

def delete_field(embed: Embed, field_name: str):
    for i in range(len(embed.fields)):
        field = embed.fields[i]
        if field.name == field_name:
            embed.remove_field(i)
    return embed

def check_if_it_is_skye(interaction: Interaction):
    return interaction.user.id == 806334528230129695

def text_to_num(text: str):
    text = text.lower()
    text = text.split()
    gold = 0
    for i in text:
        d = {
            'k': 1000,      # thousands
            'm': 1000000,   # millions
            'b': 1000000000 # billions
        }
        i = i.lower()
        if not isinstance(i, str):
            # Non-strings are bad are missing data in poster's submission
            return False
        elif i[-1] in d:
            # separate out the K, M, or B
            num, magnitude = i[:-1], i[-1]
            gold += int(num) * d[magnitude]
        elif i.isnumeric():
            gold += int(i)
        else:
            return False
    return gold

def get_mapping(interaction: Interaction):
    mapping = {}
    for cog_name, cog in bot.cogs.items():
        commands = []
        for application_cmd in cog.to_register:
            cmd_in_guild = False
            if application_cmd.is_global:
                cmd_in_guild = True
            elif interaction.guild_id in application_cmd.guild_ids:
                cmd_in_guild = True
            if cmd_in_guild == True:
                commands.append(application_cmd)
        if len(commands) != 0:
            mapping[cog_name] = (cog, commands)
    return mapping
    
def get_all_item_names():
    sql = """
    SELECT name
    FROM items
    """
    cursor = db.execute_query(sql)
    return cursor.fetchall()[0]

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
    time = {
        "d": 0, 
        "h": 0,
        "m": 0,
        "s": round(error.retry_after)
    }
    while time["s"] >= 60:
        time["m"] += 1
        time["s"] -= 60
    while time["m"] > 60:
        time["h"] += 1
        time["m"] -= 60
    while time["h"] > 24:
        time["d"] += 1
        time["h"] -= 24
    time_txt = ""
    for i in time:
        if time[i] != 0:
            time_txt += f"{time[i]}{i} "
    cd_ui.description = f"Wait **{time_txt}** before using `{ctx.clean_prefix}{ctx.command.qualified_name}` again."
    cd_ui.colour = random.choice(embed_colours)
    return cd_ui

@bot.event
async def on_command_error(ctx: commands.Context, error):
    code_error = False
    if isinstance(error, commands.errors.CheckFailure):
        if ctx.command.cog_name == "Dev Only":
            await ctx.send("Only devs can use this command.\nOn the plus side, maybe this will be introduced to the game later!", delete_after=3)
        elif ctx.command.cog_name == "BNB Only":
            if ctx.guild.id != 827537903634612235:
                await ctx.send(content="This command is only available in the BNB server.", delete_after=3)
            elif ctx.channel.id != 836212817711333426:
                await ctx.send(content="This command is only available in <#836212817711333426>.", delete_after=3)
            else:
                await ctx.send(content="This command is only available to mods.", delete_after=3)
        else:
            await ctx.send("You are missing the role(s)/permission(s) to use this command.", delete_after=3)
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=cd_embed(ctx, error), delete_after=3)
    else:
        code_error = True
        raise error
    if not code_error:
        try:
            await ctx.message.delete()
        except(nextcord.HTTPException):
            ctx.guild.owner.send(f"I don't have the correct perms in your server! Try checking my profile and re-add me to your server.\n`Server` - `{ctx.guild.name}`")

@bot.event
async def on_application_command_error(interaction: Interaction, error):
    if isinstance(error, commands.errors.CheckFailure):
        await interaction.response.send_message("You are missing the role(s)/permission(s) to use this command.", ephemeral=True)
    elif isinstance(error, commands.CommandOnCooldown):
        await interaction.response.send_message(embed=cd_embed(interaction, error), ephemeral=True)
    else:
        raise error

bot.run(TOKEN)