import os
import nextcord
import random
import main
import math 
from main import bot
from datetime import datetime
from nextcord.ext import commands
from nextcord import Embed
from nextcord.ui import Button, View
import database as db
from typing import Optional
from functions.users import Users
from views.currency_views import EndInteraction, generate, MultiplePages
class Currency(commands.Cog, name="Currency"):
    
    COG_EMOJI = "🪙"

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="users")
    async def usersview(self, ctx):
        sql = "SELECT * from users"
        cursor = db.execute_query(sql)
        await ctx.send("Users:")
        for row in cursor.fetchall():
            await ctx.send(row)

    @commands.command(name="create")
    async def create(self, ctx):
        """Create your own profile to start playing the Build & Battle game!"""
        users = Users(ctx.author)
        if not(users.if_user_present()):
            users.update_user_profile((ctx.author.id, 1000, 1000))
            db.conn.commit()
            await ctx.send("Profile sucessfully created! Check your profile with `+profile`!")
        else:
            await ctx.send("WTF are you thinking? You are already a player and you are creating another player?!")

    @commands.command(name="profile")
    async def profile(self, ctx, user: nextcord.Member=None):
        """Check the profile of your own or others.
        If you left the `[user]` parameter blank, the bot shows your own profile.
        Otherwise, it shows other users" profiles."""
        if user == None:
            user = ctx.author
        users = Users(user)
        if users.if_user_present():
            user_profile = users.get_user_profile()
            print(user_profile)
            print(f"Gold: {user_profile[1]}")
            print(f"XP: {user_profile[2]}")
            profile_ui = Embed()
            profile_ui.colour = random.choice(main.embed_colours)
            profile_ui.set_author(name=f"{user.name}'s Profile:", icon_url=user.avatar)
            profile_ui.add_field(name="Gold", value=f'${user_profile[1]}', inline=False)
            profile_ui.add_field(name="XP", value=f'{user_profile[2]}/{main.roundup(user_profile[2], 100) if user_profile[2] != 0 else 100}', inline=False)
            # farm_width = main.rounddown(user_profile["xp"], 100) / 100 + 2
            # if farm_width >= 12:
            #     farm_width = 12
            # profile_ui.add_field(name="Farm Size", value=int(pow(farm_width, 2)), inline=False)
            profile_msg = await ctx.send(embed=profile_ui)
        else:
            await ctx.send("The user do not have a profile! Create one with `+create`")
        
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
        view = generate(ctx)
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
                            name = "hi"
                            )
                page.add_field(
                            name = "Page B",
                            value = "I'll add something"
                            )
                return page
            
            def page_ui_c(self):
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
                page.add_field(
                    name = "Page A",
                    value = "Select the page you want to see."
                )
                return page
            
            async def keith_sucks(self):
                page = Embed()
                hoho = await bot.fetch_user(798720829583523861)
                page.set_author(
                            name = hoho.name,
                            icon_url = hoho.avatar
                            )
                page.add_field(
                            name = "Page B",
                            value = "Keith sucks."
                            )
                return page
            
            def everything(self):
                page = Embed()
                page.set_author(
                            name = bot.user.name,
                            icon_url = bot.user.avatar
                            )
                page.add_field(
                            name = "Everything can be completely different",
                            value = "i made one using buttons check it out with `advanced_cmd`"
                            )
                return page
        pages = Pages(ctx)
        view = MultiplePages(ctx, pages)
        view.message = await ctx.send(embed=pages.something(), view=view)


def setup(bot: commands.Bot):
    bot.add_cog(Currency(bot))