import os
import nextcord
import random
import main
from main import bot
from datetime import datetime
from nextcord.ext import commands
from nextcord import Embed
from nextcord.ui import Button, View
import database as db
from typing import Optional
from functions.users import Users
from views.currency_views import EndInteraction, Generate, MultiplePages, PagesWithSelect
class Currency(commands.Cog, name="Currency"):
    
    COG_EMOJI = "🪙"

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None 

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

    @commands.command(name="profile")
    async def profile(self, ctx, user: nextcord.Member=None):
        """Check the profile of your own or others.
        If you left the `[user]` parameter blank, the bot shows your own profile.
        Otherwise, it shows other users" profiles."""
        if user == None:
            user = ctx.author
        users = Users(user)
        if users.if_user_present() == False:
            users.create_user_profile()
        user_profile = users.get_user_profile()
        await ctx.send(user_profile)
        profile_ui = Embed()
        profile_ui.colour = random.choice(main.embed_colours)
        profile_ui.set_author(name=f"{user.name}'s Profile:", icon_url=user.avatar)
        await ctx.send("author")
        profile_ui.add_field(name="Gold", value=f'${user_profile["user"]["gold"]}', inline=False)
        await ctx.send("gold")
        xp = int(user_profile["user"]["xp"])
        profile_ui.add_field(name="XP", value=f'{xp}/{main.roundup(xp, 100) if xp != 0 else 100}', inline=False)
        await ctx.send("xp")
        profile_ui.add_field(name="Farm Width", value=f'{user_profile["farm"]["farm_width"]} crops', inline=False)
        await ctx.send("width")
        profile_ui.add_field(name="Farm Height", value=f'{user_profile["farm"]["farm_height"]} crops', inline=False)
        await ctx.send("height")
        profile_msg = await ctx.send(embed=profile_ui)
        
    @commands.command(name="buttons")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def buttons(self, ctx):
        """uh... so this is a test for buttons, that i'm gonna implement it in the bot
        ||some time soon||
        """
        buttons_ui = Embed()
        buttons_ui.color = random.choice(main.embed_colours)
        buttons_ui.set_author(name=bot.user.name, icon_url=bot.user.avatar)
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
                            name = bot.user.name,
                            icon_url = bot.user.avatar
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
                hoho = await bot.fetch_user(798720829583523861)
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
                            name = bot.user.name,
                            icon_url = bot.user.avatar
                            )
                page.title = "Page 3 - Everything can be completely different"
                page.description = "i made one using buttons check it out with `+advanced_cmd`"
                return page
        pages = Pages(ctx)
        view = PagesWithSelect(ctx, pages)
        view.message = await ctx.send(embed=pages.something(), view=view)


def setup(bot: commands.Bot):
    bot.add_cog(Currency(bot))