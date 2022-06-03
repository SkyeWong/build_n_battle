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
from views.dev_views import EmojiView, EditItemView

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

    @nextcord.slash_command(name="modify", guild_ids=[main.DEVS_SERVER_ID])
    async def edit(self, interaction: Interaction):
        """Modify users and items info.
        Should not be called."""
        pass

    @edit.subcommand(name="user", inherit_hooks=True)
    async def user(self, interaction: Interaction):
        """Edit a user's profile.
        Should not be called."""
        pass
    
    @user.subcommand(name="gold", description="Modify or set a user's gold", inherit_hooks=True)
    async def gold(
        self, 
        interaction: Interaction, 
        gold: str = SlashOption(
            name = "gold",
            required = True
        ),
        user: nextcord.Member = SlashOption(
            name = "user",
            required = False,
            default = None
        ),
        set_or_modify: int = SlashOption(
            name = "set-or-modify",
            description = "Changes the user's gold by a certain value or sets it to the value. DEFAULT: MODIFY",
            choices = {
                "set": 0,
                "modify": 1
            },
            required = False,
            default = 1
        )
    ):
        if user == None:
            user = interaction.user
        users = Users(user)
        gold = main.text_to_num(gold)
        if gold:
            if set_or_modify == 0:
                users.set_gold(gold)
                await interaction.response.send_message(f"set {user.display_name}'s gold to {gold}", ephemeral=True)
            else:
                new_gold = users.modify_gold(gold)
                await interaction.response.send_message(f"set {user.display_name}'s gold to {new_gold}, modified by {gold}", ephemeral=True)
            skye = await bot.fetch_user(806334528230129695)
            await skye.send(f"{interaction.user.name} set {user.name} to {gold}")
        else:
            await interaction.response.send_message("can't set the gold to that, try again")

    @edit.subcommand(name="item", inherit_hooks=True)
    async def item(self, interaction: Interaction):
        """Add, edit, or delete an item."""
        pass

    @item.subcommand(name="edit", description="Edit an item's name, description, trade price etc", inherit_hooks=True)
    async def item(
        self, 
        interaction: Interaction,
        itemname: str = SlashOption(
            description="The item to edit",
            choices = main.get_all_item_names()
        )
    ):
        sql = """
            SELECT id, name, description, emoji_name, emoji_id, buy_price, sell_price, trade_price
            FROM items
            WHERE name LIKE %s or emoji_name LIKE %s
            ORDER BY name ASC
            LIMIT 1
        """
        cursor = db.execute_query_dict(sql, (f"%{itemname}%",) * 2)
        results = cursor.fetchall()
        if len(results) == 0:
            await interaction.send("The item is not found!")
        else:
            embed = Embed()
            item = results[0]
            embed.colour = random.choice(main.embed_colours)
            embed.title = "Current values of "
            embed.title += item["name"]
            embed.description = ">>> "
            embed.description += item["description"]
            embed.description += f"\n\n**BUY** - {item['buy_price']}\n**SELL** - {item['sell_price']}\n**TRADE** - {item['trade_price']}"
            embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{item['emoji_id']}.png")
            view = EditItemView(interaction, item["id"])
            await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(dev_only(bot))

