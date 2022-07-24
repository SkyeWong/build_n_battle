import os
import nextcord
import random
import main
from datetime import datetime
from nextcord.ext import commands
from nextcord import Embed, Interaction, SlashOption
from nextcord.ui import Button, View
import database as db
from typing import Optional
from functions.users import Users
from views.currency_views import EndInteraction, Generate, MultiplePages, PagesWithSelect

class Currency(commands.Cog, name="Currency"):
    
    COG_EMOJI = "🪙"

    def __init__(self):
        self._last_member = None 

    async def cog_application_command_before_invoke(self, interaction: Interaction):
        users = Users(interaction.user)
        if users.if_user_present() == False:
            users.create_user_profile()
    
    @commands.command(name="create")
    async def create(self, ctx):
        """Create your own profile to start playing the Build & Battle game!"""
        users = Users(ctx.author)
        if not(users.if_user_present()):
            users.update_user_profile({
                "user": {
                    "id": ctx.author.id,
                    "gold": 1000,
                    "xp": 0
                },
                "farm": {
                    "crops": '["","","",""]',
                    "crop_type": '["","","",""]',
                    "farm_width": 2,
                    "farm_height": 2
                },
                "commands_last_used": {
                    "farm": int(datetime.now().timestamp())
                }
            })
            await ctx.send("Profile sucessfully created! Check your profile with `+profile`!")
        else:
            await ctx.send("You are already a player!")

    @nextcord.slash_command(name="profile")
    async def profile(
        self,
        interaction: Interaction, 
        user: nextcord.Member = SlashOption(
            name = "user",
            description = "The user to check the profile",
            required = False,
            default = None
        )):
        """Check the profile of your own or others."""
        if user == None:
            user = interaction.user
        users = Users(user)
        if users.if_user_present() == False:
            users.create_user_profile()
        user_profile = users.get_user_profile()
        profile_ui = Embed()
        profile_ui.colour = random.choice(main.embed_colours)
        profile_ui.set_thumbnail(url=user.display_avatar.url)
        profile_ui.set_author(name=f"{user.name}'s Profile:")
        profile_ui.add_field(name="Gold", value=f'${user_profile["user"]["gold"]}', inline=False)
        xp = int(user_profile["user"]["xp"])
        profile_ui.add_field(name="XP", value=f'{xp}/{main.roundup(xp, 100) if xp != 0 else 100}', inline=False)
        profile_ui.add_field(name="Farm Width", value=f'{user_profile["farm"]["farm_width"]} crops', inline=False)
        profile_ui.add_field(name="Farm Height", value=f'{user_profile["farm"]["farm_height"]} crops', inline=False)
        profile_msg = await interaction.send(embed=profile_ui)

    @nextcord.slash_command(name="item", guild_ids=[main.DEVS_SERVER_ID])
    async def item(
        self, 
        interaction: Interaction, 
        itemname: str = SlashOption(
            description = "The item to search for",
            choices = main.get_all_item_names()
        )
    ):
        """Get information of an item."""
        sql = """
            SELECT name, description, emoji_name, emoji_id, buy_price, sell_price, trade_price
            FROM items
            WHERE name LIKE %s or emoji_name LIKE %s
            ORDER BY name ASC
            LIMIT 1
        """
        cursor = db.execute_query(sql, (f"%{itemname}%",) * 2)
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
            # **rarity**
            # 0 - common
            # 1 - uncommon
            # 2 - rare
            # 3 - epic
            # 4 - legendary
            # 5 - godly
            rarity = ["common", "uncommon", "rare", "epic", "legendary", "godly"]
            embed.add_field(name="Rarity", value=rarity[item["rarity"]])
            embed.set_thumbnail(url=f"https://cdn.discordapp.com/emojis/{item['emoji_id']}.png")
            await interaction.send(embed=embed)
        
    @commands.command(name="buttons")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def buttons(self, ctx: commands.Context):
        """uh... so this is a test for buttons, that i'm gonna implement it in the bot
        ||some time soon||
        """
        buttons_ui = Embed()
        buttons_ui.colour = random.choice(main.embed_colours)
        buttons_ui.set_author(name=ctx.bot.user.name, icon_url=ctx.bot.user.avatar)
        buttons_ui.description = "Click the buttons below to test the buttons."
        view = Generate(ctx)
        view.message = await ctx.send(embed=buttons_ui, view=view)

    @commands.command(name="viewtest")
    async def viewtest(self, ctx):
        view = EndInteraction()
        await ctx.send("Test:\n`absolutely nothing :)`", view=view)
    
    @commands.command(name="advanced_cmd")
    async def advanced_cmd(self, ctx):
        """A command including multiple pages that you can switch to!
        The name is from Keith, not me."""
        class Pages():
            def __init__(self, ctx):
                self.ctx = ctx
            
            def page_ui_a(self):
                page = Embed()
                page.set_author(
                    name = self.ctx.author.name,
                    icon_url = self.ctx.author.avatar
                )
                page.add_field(
                    name = "Page A",
                    value = "Select the page you want to see."
                )
                return page
            
            def page_ui_b(self):
                page = Embed()
                page.set_author(
                            name = ctx.bot.user.name,
                            icon_url = ctx.bot.user.avatar
                            )
                page.add_field(
                            name = "Everything can be completely different",
                            value = "idk what are you doing if ure here"
                            )
                return page
        pages = Pages(ctx)
        view = MultiplePages(ctx, pages)
        view.message = await ctx.send(embed=pages.page_ui_a(), view=view)

    @commands.command(name="pagesbutselect")
    async def pagesbutselect(self, ctx):
        class Pages():
            def __init__(self, ctx):
                self.ctx = ctx
            
            def something(self):
                page = Embed()
                page.set_author(
                    name = self.ctx.author.name,
                    icon_url = self.ctx.author.avatar
                )
                page.title = "Page 1 - Something in somewhere"
                page.description = "Select the page you want to see."
                return page
            
            async def keith_sucks(self):
                page = Embed()
                hoho = await ctx.bot.fetch_user(798720829583523861)
                page.set_author(
                            name = hoho.name,
                            icon_url = hoho.avatar
                            )
                page.title =  "Page 2 - Nothing. Really."
                page.description = "Keith sucks."
                return page
            
            def everything(self):
                page = Embed()
                page.set_author(
                            name = ctx.bot.user.name,
                            icon_url = ctx.bot.user.avatar
                            )
                page.title = "Page 3 - Everything can be completely different"
                page.description = "i made one using buttons check it out with `+advanced_cmd`"
                return page
        pages = Pages(ctx)
        view = PagesWithSelect(ctx, pages)
        view.message = await ctx.send(embed=pages.something(), view=view)


def setup(bot: commands.Bot):
    bot.add_cog(Currency())