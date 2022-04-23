import os
from discord import SlashOption
from nextcord import ButtonStyle
import nextcord
import json 
from datetime import datetime
import random
import asyncio
import main
from main import bot
from nextcord.ext import commands, tasks
from nextcord import Embed, Interaction
from nextcord.ui import Button, View
import database as db

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
                if emojiname in emoji.name or emojiname == emoji.id:
                    emojis_found.append(emoji)
            if emojis_found != []:
                await interaction.response.send_message(f"There are `{len(emojis_found)}` results for `{emojiname}`.")
                embed = Embed()
                embed.set_author(name="Emoji Searcher:", icon_url=bot.user.display_avatar.url)
                embed.colour = random.choice(main.embed_colours)
                for emoji in emojis_found:
                    embed.clear_fields()
                    embed.title = f"`{emojis_found.index(emoji) + 1}` - click for emoji"
                    embed.url = emoji.url
                    embed.description = f"{emoji}"
                    field =f">>> ➼ `Name` - :{emoji.name}:"
                    field += f"\n➼ `Guild` - {emoji.guild.name}"
                    field += f"\n➼ `ID`    - {emoji.id}"
                    field += f"\n➼ `Url`   - [{emoji.url}]({emoji.url})"
                    field += f"\n➼ `Usage` - <\:{emoji.name}:{emoji.id}>"
                    embed.add_field(name=f":{emoji.name}:", value=field)
                    await interaction.followup.send(embed=embed)
                if len(emojis_found) > 3:
                    url = await interaction.original_message()
                    await interaction.followup.send(f"Jump - {url.jump_url}")
            else:
                await interaction.response.send_message(f"No emoji is found for `{emojiname}`.", delete_after=5)

    @nextcord.slash_command(name="no-of-players", description="Shows the number of users in BNB.")
    async def no_of_players(self, interaction: Interaction):
        sql = "SELECT COUNT(id) AS NoOfUsers FROM users"
        cursor = db.execute_query(sql)
        await interaction.response.send_message(cursor.fetchall()[0])
        sql = f"""
            SELECT id, gold
            FROM users
            ORDER BY gold DESC
            LIMIT 5
        """
        cursor = db.execute_query(sql)
        await interaction.followup.send("richest players:")
        for record in cursor.fetchall():
            await interaction.followup.send(f"{bot.fetch_user(record[0])}: {record[1]} gold")

def setup(bot: commands.Bot):
    bot.add_cog(dev_only(bot))

