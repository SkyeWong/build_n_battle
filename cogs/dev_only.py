from nextcord import ButtonStyle
import nextcord
from datetime import datetime
import random
import asyncio
import main
import math
from main import bot
from nextcord.ext import commands, tasks, application_checks
from nextcord import Embed, Interaction, SlashOption
from nextcord.ui import Button, View
import database as db
from functions.users import Users
from views.dev_views import EmojiView, EditItemView
from mysql.connector import Error

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

    @item.subcommand(name="add", description="Add a new item into the game", inherit_hooks=True)
    async def add_item(
        self,
        interaction: Interaction,
        name: str = SlashOption(required=True),
        description: str = SlashOption(required=True),
        emoji_name: str = SlashOption(required=True),
        emoji_id: str = SlashOption(required=True),
        rarity: int = SlashOption(
            choices = {
                "common": 0,
                "uncommon": 1,
                "rare": 2,
                "epic": 3,
                "legendary": 4,
                "godly": 5
            }, 
            required=True
        ),
        buy_price: int = SlashOption(required=False, default=0),
        sell_price: int = SlashOption(required=False, default=0),
        trade_price: int = SlashOption(required=False, default=0),
    ):
        errors = []
        prices = [buy_price, sell_price, trade_price]
        for index, price in enumerate(prices):
            # if the value is NULL, change it to None
            if price == 0:
                prices[index] = None
            else:
                # if value in one of these convert them from "2k" to 2000
                prices[index] = str(main.text_to_num(self.input.value))
            if prices[index] == False:
                errors.append("This is not a valid number. Tip: use `2k` for _2,000_, `5m 4k` for _5,004,000_")
        # if value is name max length = 30
        if name and len(name) > 30:
            errors.append("The name must not be more than 30 characters in length.")
        # if value is description max length = 100
        if description and len(description) > 100:
            errors.append("The description must not be more than 100 characters in length.")
        # change emoji id to int
        if not emoji_id.isnumeric():
            errors.append("The emoji id is invalid")
        # if it is an invalid value send a message and return the function
        if len(errors) > 0:
            msg = "The following errors occured:"
            for i in errors:
                msg += f"\n{i}"
            await interaction.send(msg, ephemeral=True)
            return
        sql = """
            INSERT INTO items (name, description, emoji_name, emoji_id, buy_price, sell_price, trade_price, rarity)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor = db.execute_query(sql, (name, description, emoji_name, emoji_id, buy_price, sell_price, trade_price, rarity))
            db.conn.commit()
        except (AttributeError, Error) as error:
            await interaction.send("either you entered an invalid value or an internal error occured.", ephemeral=True)
            raise error
        embed = Embed()
        embed.title = f"Added {name}"
        embed.colour = random.choice(main.embed_colours)
        embed.description = ">>> "
        embed.description += description
        embed.description += f"\n\n**BUY** - {buy_price}\n**SELL** - {sell_price}\n**TRADE** - {trade_price}"
        # **rarity**
        # 0 - common
        # 1 - uncommon
        # 2 - rare
        # 3 - epic
        # 4 - legendary
        # 5 - godly
        rarities = ["common", "uncommon", "rare", "epic", "legendary", "godly"]
        embed.add_field(name="Rarity", value=rarities[rarity])
        embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{emoji_id}.png")
        await interaction.send(embed=embed)

    @item.subcommand(name="edit", description="Edit an item's name, description, trade price etc", inherit_hooks=True)
    async def edit_item(
        self, 
        interaction: Interaction,
        itemname: str = SlashOption(
            description="The item to edit",
            choices = main.get_all_item_names()
        )
    ):
        sql = """
            SELECT id, name, description, emoji_name, emoji_id, buy_price, sell_price, trade_price, rarity
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
            item = results[0]
            view = EditItemView(interaction, item["id"])
            embed = view.get_item_embed()
            await interaction.send(embed=embed, view=view)

    @nextcord.slash_command(name="dm-spam", description="DM spam a user with the message and the amount of times.", guild_ids=[main.DEVS_SERVER_ID])
    async def dm_spam(
        self, 
        interaction: Interaction, 
        user: nextcord.User = SlashOption(
            description = "the id of that user", 
            required = True
        ),
        message: str = SlashOption(
            description = "the msg to show",
            required = True
        ),
        times: int = SlashOption(
            description = "spam him for how many times?", 
            required = True,
            min_value = 1, 
            max_value = 5000
        ),
        show_author: int = SlashOption(
            name = "show-author",
            description = "show who spammed him or not (showing who spammed is not a good idea)",
            choices = {
                "YESSSS": 1,
                "NOOOOO": 0
            },
            default = 1,
            required = False
        ),
        time_interval: float = SlashOption(
            name = "time-interval",
            description = "number of seconds between a select number of messages. defaults to 1",
            default = 1, 
            required = False,
            min_value = 0,
            max_value = 15
        ),
        between_time_interval: int = SlashOption(
            name = "between-time-interval",
            description = "messages sent between each time interval. unadvised to set this too high. undefaults to 1",
            default = 1,
            required = False
        ),
        userid: str = SlashOption(
            description = "the id of that user. if this is set, this overrides the User option.", 
            required = False
        ),
    ):
        if userid:
            if userid.isnumeric():
                userid = int(userid)
            else:
                await interaction.send("not a valid id", ephemeral=True)
                return
            try:
                user = await bot.fetch_user(userid)
            except:
                await interaction.send("user not found", ephemeral=True)
                return
        await interaction.send("||fuck you||", delete_after=0.05)
        str_len = len(str(times))
        embed = Embed()
        embed.colour = random.choice(main.embed_colours)
        embed.title = f"Spamming {user.name}..."
        embed.add_field(name=f"Message", value=message)
        embed.add_field(name=f"Total number of messages", value=times)
        embed.add_field(name=f"Time intervals", value=f"{between_time_interval} times every {time_interval} sec")
        estimated_finish_time = int(math.ceil(datetime.now().timestamp() + math.ceil(times / between_time_interval) * time_interval))
        embed.add_field(name=f"Estimated finishing time", value=f"<t:{estimated_finish_time}:R> | <t:{estimated_finish_time}:F>")
        embed.set_footer(text="The estimated finishing time may be inaccurate (too early) bcs of lag")
        notify_author = await interaction.user.send(embed=embed)
        messages_sent = 1
        for i in range(math.ceil(times / between_time_interval)):
            for j in range(between_time_interval):
                if messages_sent <= times:
                    msg = f"`{(str_len - len(str(messages_sent))) * '0'}{messages_sent}` - `{message}`"
                    msg += f" from `{interaction.user.name}`" if show_author == 1 else ""
                    await user.send(msg)
                    messages_sent += 1
                else:
                    break
            if messages_sent <= times:
                await asyncio.sleep(time_interval)
        embed.title = f"Spammed {user.name}!"
        embed.add_field(name="Finished spamming at", value=f"<t:{int(datetime.now().timestamp())}:R> | <t:{int(datetime.now().timestamp())}:F>")
        await notify_author.edit(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(dev_only(bot))
