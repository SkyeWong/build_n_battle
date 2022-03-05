import os
import nextcord
import json
import random
import asyncio
import main
import math 
from main import bot
from datetime import datetime
from nextcord.ext import commands, tasks
import database as db

weathers = ["sunny", "rainy", "stormy", "windy", "snowy"]
crop_emojis = ["<:crop_1:919601339464560650>", "<:crop_2:919601339338735616>", "<:crop_3:919601339082879027>", "<:crop_4:919601339456180264>", "<:crop_5:919601339447799848>"]
i = 10
crop_progress = []
while i <= 16:
    crop_progress.append(i / 1000)
    i += 1

class build_and_battle(commands.Cog, name="Build & Battle"):
    """My game! 
    ~~i can\"t think of this it will be done later~~
    """

    COG_EMOJI = "🎮"

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    def if_user_present(self, user):
        sql = f"""
            SELECT id, gold, xp
            FROM users
            WHERE id = {user.id};
            """
        cursor = db.execute_query(sql)
        if cursor.fetchall() != []:
            return True
        else:
            return False

    def get_user_profile(self, user):
        sql = f"""
            SELECT id, gold, xp
            FROM users
            WHERE id = {user.id};
            """
        cursor = db.execute_query(sql)
        return cursor.fetchall()[0]

    def update_user_profile(self, user, new_profile):
        sql = "INSERT INTO users (id, gold, xp) VALUES (%s, %s, %s)"
        print(new_profile)
        with db.cursor() as cursor:
            cursor.execute(sql, new_profile)
            db.commit()
        # user_profile_list = self.get_user_profile_list()
        # users = self.get_user_list()
        # for i in new_profile["crops"]:
        #     new_profile["crops"][new_profile["crops"].index(i)] = str(i)
        # new_profile["crops"] = ", ".join(new_profile["crops"])
        # if self.if_user_present(user):
        #     user_profile_list[users.index(user.id)] = new_profile
        # else:
        #     user_profile_list.append(new_profile)
        # with open("user_profile.json", "w+") as f:
        #     json.dump(user_profile_list, f, indent=4)
        # return new_profile
    
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
        if not(self.if_user_present):
            sql = "INSERT INTO users (id, gold, xp) VALUES (%s, %s, %s)"
            val = (ctx.author.id, 1000, 1000)
            cursor = db.execute_query(sql, val)
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
        if self.if_user_present(user):
            user_profile = self.get_user_profile(user)
            print(user_profile)
            print(f"Gold: {user_profile[1]}")
            print(f"XP: {user_profile[2]}")
            profile_ui = nextcord.Embed()
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

    # def update_farm_ui(self, user):
    #     user_profile = self.get_user_profile(user)
    #     sent_time = int(datetime.now().timestamp())
    #     with open("weathers.json", "r") as f:
    #         weather_list = json.load(f)
    #     past_weather = weather_list[-(math.floor((sent_time - user_profile["farm_last_used"]) / 60 / 60)):]
    #     grow_speed = 1
    #     for i in past_weather:
    #         if i == "sunny":
    #             grow_speed *= 1.15
    #         elif i == "stormy":
    #             grow_speed *= 0.8
    #         elif i == "rainy":
    #             grow_speed *= 1.3
    #         elif i == "windy":
    #             grow_speed *= 0.95
    #         elif i == "snowy":
    #             grow_speed *= 0.85
    #     for i in range(len(user_profile["crops"])):
    #         user_profile["crops"][i] += (sent_time - user_profile["farm_last_used"]) / 60 * random.choice(crop_progress) * grow_speed
    #         if user_profile["crops"][i] >= 4.5:
    #             user_profile["crops"][i] = 5.0
    #     test = user_profile["farm_last_used"]
    #     user_profile["farm_last_used"] = sent_time
    #     crop = ""
    #     farm_ui = nextcord.Embed()
    #     farm_ui.set_author(name=f"{user.name}\"s Farm:", icon_url=user.avatar)
    #     farm_ui.description = ""
    #     index = 0
    #     farm_width = main.rounddown(user_profile["xp"], 100) / 100 + 2
    #     if farm_width > 12:
    #         farm_width = 12
    #     farm_width = int(farm_width)
    #     crops_to_modify = abs(pow(farm_width, 2) - len(user_profile["crops"]))
    #     if pow(farm_width, 2) > pow(user_profile["farm_width"], 2):
    #         farm_ui.add_field(name="Your farm expanded!", value=f"Now your farm has {pow(farm_width, 2)} crops.", inline=False)
    #         for i in range(crops_to_modify):
    #             user_profile["crops"].append(1)
    #     if pow(farm_width, 2) < pow(user_profile["farm_width"], 2):
    #         farm_ui.add_field(name="Your farm shrunk!", value=f"Sorry for the inconvinence. We think that\"s a bug. Now your farm has {pow(farm_width, 2)} crops.", inline=False)
    #         for i in range(crops_to_modify):
    #             user_profile["crops"].pop()
    #     for y in range(farm_width):
    #         for x in range(farm_width):
    #             crop = user_profile["crops"][index]
    #             crop = round(crop)
    #             farm_ui.description += crop_emojis[crop - 1]
    #             index += 1
    #         farm_ui.description += "\n"
    #     user_profile["farm_width"] = farm_width
    #     with open("weathers.json", "r") as f:
    #         weather_list = json.load(f)
    #     farm_ui.colour = random.choice(main.embed_colours)
    #     farm_ui.add_field(name="Dev Data", value=f"Grow Speed: {grow_speed}\nPast Weather: {past_weather}\nFarm last used: {test}\nSent time: {sent_time}")
    #     farm_ui.set_footer(text=f"weather: {weather_list.pop()}")
    #     user_profile = self.update_user_profile(user, user_profile)
    #     user_profile = self.get_user_profile(user)
    #     return farm_ui, user_profile

    # @commands.command(name="farm", help="Farming!")
    # async def farm(self, ctx):
    #     if self.if_user_present(ctx.author):
    #         farm_ui, user_profile = self.update_farm_ui(ctx.author)
    #         farm_embed = await ctx.send(embed=farm_ui)
    #         if ctx.author == ctx.author:
    #             emojis = ["🌾", "⏹"]
    #         else:
    #             emojis = ["⏹️"]
    #         for emoji in emojis:
    #             await farm_embed.add_reaction(emoji)
    #         reacted_emoji = ""
    #         while reacted_emoji != "⏹️":
    #             def check(reaction, user):
    #                 for emoji in emojis:
    #                     if str(reaction.emoji) == emoji:
    #                         correct_emoji = True
    #                 return user == ctx.author and correct_emoji
    #             try:
    #                 reaction, user = await bot.wait_for("reaction_add", timeout=15.0, check=check)
    #             except asyncio.TimeoutError:
    #                 break
    #             else:
    #                 reacted_emoji = str(reaction.emoji)
    #                 await farm_embed.remove_reaction(reaction.emoji, ctx.author)
    #                 farm_ui, user_profile = self.update_farm_ui(ctx.author)
    #                 fully_grown_crops = 0
    #                 if reacted_emoji == "🌾":
    #                     for i in user_profile["crops"]:
    #                         if i == 5:
    #                             fully_grown_crops += 1
    #                             user_profile["crops"][user_profile["crops"].index(i)] = 1
    #                     earned_gold = 10 * fully_grown_crops
    #                     earned_xp = random.choice(range(1, 9)) * fully_grown_crops
    #                     user_profile["gold"] += earned_gold
    #                     user_profile["xp"] += earned_xp
    #                     self.update_user_profile(ctx.author, user_profile)
    #                     farm_ui, user_profile = self.update_farm_ui(ctx.author)
    #                     farm_ui.add_field(name="Crop collected and sold!", value=f"You sold {fully_grown_crops} fully grown crop(s) so you earned ${earned_gold} and {earned_xp} XP!", inline=False)
    #                     await farm_embed.edit(embed=farm_ui)
    #         for emoji in emojis:
    #             await farm_embed.remove_reaction(emoji, bot.user)
    #     else:
    #         await ctx.send("You do not have a profile! Create one with `+create`")
    
    # @tasks.loop(minutes=1.0, reconnect=True)
    # async def new_weather():
    #     with open("weathers.json", "r") as f:
    #         weather_list = json.load(f)
    #     if len(weather_list) > 48:
    #         weather_list = []
    #     if datetime.now().minute == 0 or weather_list == []:
    #         current_weather = random.choice(weathers)
    #         weather_list.append(current_weather)
    #         with open("weathers.json", "w+") as f:
    #             json.dump(weather_list, f, indent=4)
    
def setup(bot: commands.Bot):
    bot.add_cog(build_and_battle(bot))
