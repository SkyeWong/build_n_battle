import os
from nextcord import ButtonStyle
import nextcord
import json 
from datetime import datetime
import random
import asyncio
import main
from main import bot
from nextcord.ext import commands, tasks, application_checks
from nextcord import Embed, Interaction, SlashOption
from nextcord.ui import Button, View
import database as db
from functions.users import Users
from views.dev_views import EmojiView

class dev_only(commands.Cog, name="Dev Only"):
    """Commands only for the devs."""

    COG_EMOJI = "👨‍💻"
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    async def cog_check(self, ctx: commands.Context):
        #Check if user is owner and return it back
        return ctx.author.id in bot.owner_ids
    
    async def cog_application_command_check(self, interaction: Interaction):
        return interaction.user.id in bot.owner_ids

    @nextcord.slash_command(name="dm", description="Send a message!", guild_ids=[main.DEVS_SERVER_ID])
    async def dm(self, interaction: Interaction, recipient: nextcord.Member, message: str):
        if recipient.bot == True:
            await interaction.response.send_message("i don't want to msg it, its ugly")
        else:
            await recipient.send(f"{interaction.user} sent a message to you via me, {bot.user.name}:\n {message}")
            embed = Embed()
            embed.title = "DM succesfully sent!"
            embed.set_author(name=bot.user.name, icon_url=bot.user.avatar)
            embed.description = "Message details:"
            embed.colour = random.choice(main.embed_colours)
            embed.add_field(name="From:", value=interaction.user, inline=True)
            embed.add_field(name="To:", value=recipient, inline=True)
            embed.add_field(name="Message:", value=message, inline=True)
            embed.add_field(name="Sent at:", value=f'<t:{int(datetime.now().timestamp())}>', inline=True)
            embed.set_footer(text="Note: markdowns and mentions will be escaped while sending the message!")
            await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="avatar", description="Shows avatar of a user.", guild_ids=[main.DEVS_SERVER_ID])
    async def avatar(
        self, 
        interaction: Interaction, 
        user: nextcord.Member = SlashOption(
            name = "user",
            description = "The user whom you wants to have avatar shown. Defaults to... YOU!",
            required = False,
            default = None,
            verify = True
        )
    ):
        if user == None:
            user = interaction.user
        await interaction.response.send_message(f"<{user.display_avatar.url}>")
        await interaction.followup.send(user.display_avatar.url)
            
    def get_emoji_embed(self, emojis, page):
        embed = Embed()
        emoji = emojis[page - 1]
        embed.set_author(name="Emoji Searcher:", icon_url=bot.user.display_avatar.url)
        embed.colour = random.choice(main.embed_colours)
        embed.set_footer(text=f"Page {page}/{len(emojis)}")
        embed.set_thumbnail(url=emoji.url)
        embed.clear_fields()
        embed.title = f"`{page}` - click for emoji"
        embed.url = emoji.url
        embed.description = f"{emoji}"
        field =f">>> ➼ `Name` - :{emoji.name}:"
        field += f"\n➼ `Guild` - {emoji.guild.name}"
        field += f"\n➼ `ID`    - {emoji.id}"
        field += f"\n➼ `Url`   - [{emoji.url}]({emoji.url})"
        field += f"\n➼ `Usage` - <\:{emoji.name}:{emoji.id}>"
        embed.add_field(name=f":{emoji.name}:", value=field)
        return embed

    @nextcord.slash_command(name="emoji", description="Search for emojis in servers the bot is in.", guild_ids=[main.DEVS_SERVER_ID])
    async def emoji(
        self, 
        interaction: Interaction,
        emojiname: str = SlashOption(
            name = "emoji",
            description = "Emoji to search for, its id or name",
            verify = True
        )):
        if len(emojiname) < 3:
            await interaction.response.send_message(content="The search term must be longer than 3 characters.", delete_after=5)
        else:
            emojis_found = [] 
            guild_emojis = []
            for guild in bot.guilds:
                for emoji in guild.emojis:
                    guild_emojis.append(emoji)
            for emoji in guild_emojis:
                if emojiname in emoji.name or emojiname == str(emoji.id):
                    emojis_found.append(emoji)
            if emojis_found != []: 
                embed = self.get_emoji_embed(emojis_found, 1)
                if len(emojis_found) > 1:
                    view = EmojiView(interaction, emojis_found, self.get_emoji_embed)
                    await interaction.response.send_message(content=f"There are `{len(emojis_found)}` results for `{emojiname}`.", embed=embed, view=view)
                else:
                    await interaction.response.send_message(content=f"There are `{len(emojis_found)}` results for `{emojiname}`.", embed=embed)
            else:
                await interaction.response.send_message(f"No emoji is found for `{emojiname}`.", delete_after=5)

    @nextcord.slash_command(name="no-of-players", description="Shows the number of users in BNB.", guild_ids=[main.DEVS_SERVER_ID])
    async def no_of_players(self, interaction: Interaction):
        sql = "SELECT COUNT(id) AS NoOfUsers FROM users"
        cursor = db.execute_query(sql)
        await interaction.response.send_message(f"There are {cursor.fetchall()[0][0]} players currently.")
        sql = f"""
            SELECT id, gold
            FROM users
            ORDER BY CONVERT(gold, DECIMAL) DESC
            LIMIT 5
        """
        cursor = db.execute_query(sql)
        richest = "5 richest players:\n>>> "
        for record in cursor.fetchall():
            user = await bot.fetch_user(record[0])
            richest += f"\n`{user.name}`・`{record[1]}⍟`"
        await interaction.followup.send(richest)

    @nextcord.slash_command(name="gold", guild_ids=[main.DEVS_SERVER_ID])
    @application_checks.check(main.check_if_it_is_skye)
    async def gold(self, interaction: Interaction):
        await interaction.send("use `/set-gold` or `/modify-gold`")
    
    @gold.subcommand(name="set-gold", guild_ids=[main.DEVS_SERVER_ID])
    @application_checks.check(main.check_if_it_is_skye)
    async def set_gold(
        self, 
        interaction: Interaction, 
        gold: str,
        user: nextcord.Member = SlashOption(
            name = "user",
            required = False,
            default = None
        )
    ):
        if user == None:
            user = interaction.user
        users = Users(user)
        gold = int(gold)
        profile = users.get_user_profile()
        profile["user"]["gold"] = gold
        users.update_user_profile(profile)
        await interaction.response.send_message(f"set {user.display_name}'s gold to {profile['user']['gold']}", ephemeral=True)

    @gold.subcommand(name="modify-gold", guild_ids=[main.DEVS_SERVER_ID])
    @application_checks.check(main.check_if_it_is_skye)
    async def modify_gold(
        self, 
        interaction: Interaction, 
        gold: str,
        user: nextcord.Member = SlashOption(
            name = "user",
            required = False,
            default = None
        )
    ):
        if user == None:
            user = interaction.user
        users = Users(user)
        gold = int(gold)
        profile = users.get_user_profile()
        profile["user"]["gold"] += gold
        profile = users.update_user_profile(profile)
        await interaction.response.send_message(f"set {user.display_name}'s gold to {profile['user']['gold']}, modified by {gold}", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(dev_only(bot))

