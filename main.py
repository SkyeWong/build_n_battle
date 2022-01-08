import os
import json 
import nextcord
import logging
from cogs import build_and_battle
from nextcord.ext import commands

TOKEN = os.environ['DISCORD_TOKEN']

logger = logging.getLogger('nextcord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='+', case_insensitive=True, activity=nextcord.Game(name='+help'), owner_id=806334528230129695)
embed_colours = [0x0071ad, 0x0064a4, 0x007dbd, 0x0096d6, 0x19afef, 0x32c8ff]

def roundup(number, round_to):
    return number if number % round_to == 0 else number + round_to - number % round_to

def rounddown(number, round_to):
    return number if number % round_to == 0 else number - number % round_to
                
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print('Connected servers/guilds:')
    for guild in bot.guilds:
        print(f'  -{guild.name}(id={guild.id})')
    #run new_weather()
    if not build_and_battle.new_weather.is_running():
        build_and_battle.new_weather.start()

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    if isinstance(message.channel, nextcord.channel.DMChannel):
        if not message.content.lower().startswith('+'):
            author = message.author.name+message.author.discriminator
            content = message.content
            sent_time = message.created_at.strftime('%A, %B %d %Y @ %H:%M:%S %p')+' UTC+0'
            message_data = [author, content, sent_time]
            with open('D:/build_n_battle-main/dm.json', 'r') as f:
                dm_messages = json.load(f)
            with open('D:/build_n_battle-main/dm_backup.json', 'r') as f:
                dm_backup_messages = json.load(f)
            dm_messages.append(message_data)
            dm_backup_messages.append(message_data)
            with open('D:/build_n_battle-main/dm.json', 'w+') as f:
                json.dump(dm_messages, f, indent=4)
            with open('D:/build_n_battle-main/dm_backup.json', 'w+') as f:
                json.dump(dm_backup_messages, f, indent=4)
    bot_id = bot.user.id
    if message.content.find(f'<@!{str(bot_id)}>') != -1:
        response = 'Hello! I\'m SkyeBot, created by Skye Wong!'
        await message.channel.send(response)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

for filename in os.listdir(os.getcwd()):
    if filename.endswith('py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.load_extension('help_cogs.cog')

bot.run(TOKEN)
