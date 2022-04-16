import os
import nextcord
import json 
from datetime import datetime
import time
import random
import asyncio
import main
from main import bot
from nextcord.ext import commands, tasks
from nextcord import Embed, Interaction, ButtonStyle, SlashOption
from nextcord.ui import Button, View

class Fun(commands.Cog, name="Fun"):

    COG_EMOJI = "🎡"

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None 

    @nextcord.slash_command(
        name = "dice", 
        description = "Roll a dice and make decisions!"
        ) 
    async def dice(
        self, 
        interaction: Interaction, 
        number_of_sides: int = SlashOption(
            name = "Number of sides in 1 die",
            required = False,
            min_value = 2,
            max_value = 10000,
            default = 6,
            verify = True
        ), 
        number_of_dice: int = SlashOption(
            name = "Number of dice",
            required = False,
            min_value = 1,
            max_value = 500,
            default = 1,
            verify = True)
    ):
        if number_of_dice == None:
            number_of_dice = 1
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        embed = nextcord.Embed()
        embed.title = f"I rolled {number_of_dice} dice(s) with {number_of_sides} sides and the result is:"
        embed.description = ", ".join(dice)
        embed.colour = random.choice(main.embed_colours)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="karson", description="Shows Karson in a big collage!")
    async def karson(self, interaction: Interaction):
        embed = nextcord.Embed()
        embed.set_image(url="https://i.ibb.co/vzRD2LC/big-collage.jpg")
        karson_user = await bot.fetch_user(708141816020729867)
        embed.set_author(name="MEET KARSON:", icon_url= karson_user.avatar)
        embed.colour = random.choice(main.embed_colours)
        await interaction.response.send_message(embed=embed)

    @commands.command(name="dicegame", brief="Play a simple dice game!", help="i will just do this later-if you sees this maybe remind me!")
    async def dicegame(self, ctx):
        money = 500
        author_avatar = ctx.author.avatar
        dice_ui = nextcord.Embed()
        dice_ui.colour = random.choice(main.embed_colours)
        dice_ui.set_author(name=f"{ctx.author.name}'s Dicegame", icon_url= author_avatar)
        dice_ui_message = await ctx.send(embed=dice_ui)
        while money > 10:
            dice_ui.insert_field_at(index=0, name="Your money left:", value=f"${money}", inline=False)
            dice_ui.insert_field_at(index=1, name="Your next guess!", value="What is your guess for the next number? Small, middle, or big?\nOr you can type \"end\" to end the game!", inline=False)
            await dice_ui_message.edit(embed=dice_ui)
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel
            guess_message = await bot.wait_for("message", check=check)
            guess = guess_message.content.lower()
            await guess_message.delete()
            dice_ui.remove_field(1)
            while guess != "small" and guess != "middle" and guess != "big" and guess != "end":
                dice_ui.remove_field(1)
                dice_ui.insert_field_at(index=1, name="Your next guess:", value="I don\"t get it. =/ Small, middle or big? Or type end to end the game!", inline=False)
                await dice_ui_message.edit(embed=dice_ui)
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel
                guess_message = await bot.wait_for("message", check=check)
                guess = guess_message.content.lower()
                await guess_message.delete()
            dice_ui.remove_field(1)
            number = random.choice(range(1, 7))+random.choice(range(1, 7))
            result = ""
            dice_ui.clear_fields()
            if guess == "small" and number <= 6:
                result = "You\"re right!"
                money += 50
            elif guess == "middle" and number == 7:
                result = "You\"re right!"
                money += 300
            elif guess == "big" and number >=8 :
                result = "You\"re right!"
                money += 50
            elif guess != "end":
                result = "Oh no! :/ It seems like you\"re wrong..."
                money -= 50
            if guess != "end":
                dice_ui.insert_field_at(index=0, name="Your money left:", value=f"${money}", inline=False)
                dice_ui.insert_field_at(index=1, name="Your guess:", value=guess, inline=False)
                await dice_ui_message.edit(embed=dice_ui)
                dice_ui.insert_field_at(index=2, name="THE SOOO IMPORTANT NUMBER:", value=number, inline=False)
                dice_ui.insert_field_at(index=3, name="THE LONG-AWAITED RESULT:", value=result, inline=False)
                dice_ui.set_footer(text="The number is produced by rolling two die together!")
            else:
                dice_ui.clear_fields()
                dice_ui.insert_field_at(index=1, name="You ended the game!", value=f"OK then :D\n You have ${money}.", inline=False)
                await dice_ui_message.edit(embed=dice_ui)
                break
            await dice_ui_message.edit(embed=dice_ui)
            time.sleep(5)
            dice_ui.clear_fields()
            dice_ui.set_footer(text="")
            await dice_ui_message.edit(embed=dice_ui)
        if money <= 10:
            await ctx.send(f"You lost! You have only ${money}...")

def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))