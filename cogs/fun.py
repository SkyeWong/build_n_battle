import os
import nextcord
import json 
from datetime import datetime
import time
import texttable
import random
import asyncio
import main
from main import bot
from nextcord.ext import commands, tasks
from nextcord import Embed, Interaction, SlashOption
from nextcord.ui import Button, View, Modal, TextInput
from views.fun_views import Analysis, HitAndBlowView, HitAndBlowData

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
        sides: int = SlashOption(
            name = "sides",
            description = "The sides of 1 die. Ranges from 2 to 50. Defaults as 6.",
            required = False,
            min_value = 2,
            max_value = 50,
            default = 6,
            verify = True
        ), 
        dice: int = SlashOption(
            name = "dice",
            description = "The number of dice. Ranges from 1 to 5000. Defaults as 1.",
            required = False,
            min_value = 1,
            max_value = 5000,
            default = 1,
            verify = True
        )
    ):
        result = [
                str(random.choice(range(1, sides + 1)))
                for _ in range(dice)
            ]
        embed = Embed()
        embed.title = f"I rolled {dice} dice with {sides} sides and the result is:"
        embed.colour = random.choice(main.embed_colours)
        if dice > 5:
            most = [0]
            least = [1]
            descr = "As there are more than 5 dice, I counted the results for you-"
            descr += "\n```css"
            for side in range(1, sides + 1):
                count = result.count(str(side))
                descr += f"\n* ({count}) [{side}s]"
                if count > result.count(str(most[0])):
                    most = [side]
                elif count == result.count(str(most[0])):
                    most.append(side)
                if count < result.count(str(least[0])):
                    least = [side]
                elif count == result.count(str(least[0])):
                    least.append(side)
            descr += "\n```"
            embed.description = descr
            view = Analysis(interaction, result, most, least)
            await interaction.response.send_message(embed=embed, view=view)
        else:
            descr = ", ".join(result)
            embed.description = descr
            await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="coinflip", description="Flip a coin!")
    async def coinflip(self, interaction: Interaction):
        embed = Embed()
        embed.title = "Flippin' a coin..."
        embed.colour = random.choice(main.embed_colours)
        result = random.choice(range(2))
        if result == 0:
            embed.set_image(url="https://i.imgur.com/lr3DjHO.gif")
        else:
            embed.set_image(url="https://i.imgur.com/An6Vm2C.gif")
        await interaction.response.send_message(embed=embed)
        embed.title = "And the result is..."
        if result == 0:
            embed.description = "**`HEADS`**"
            embed.set_image(url="https://i.imgur.com/8BSllkX.png")
            await asyncio.sleep(2)
        else:
            embed.description = "**`TAIL`**"
            embed.set_image(url="https://i.imgur.com/VcqwLpT.png")
            await asyncio.sleep(3)
        await interaction.edit_original_message(embed=embed)

    @nextcord.slash_command(name="karson", description="Shows Karson in a big collage!")
    async def karson(self, interaction: Interaction):
        embed = Embed()
        embed.set_image(url="https://i.ibb.co/vzRD2LC/big-collage.jpg")
        karson_user = await bot.fetch_user(708141816020729867)
        embed.set_author(name="MEET KARSON:", icon_url= karson_user.avatar)
        embed.colour = random.choice(main.embed_colours)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="8ball", description="I can tell you the future... make decisions! 🎱")
    async def eight_ball(
        self, 
        interaction: Interaction, 
        whattodecide: str = SlashOption(
            name = "what-to-decide"
        )
    ):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ] 
        await interaction.response.send_message(f"You shook me and some words appeared...\n```md\n# {str(random.choices(responses)[0])}\n```")

    @nextcord.slash_command(name="hit-and-blow", description="Play a fun hit & blow game!", guild_ids=[main.DEVS_SERVER_ID])
    async def hit_or_blow(
        self, 
        interaction: Interaction, 
        bet: str = SlashOption(
            name = "bet",
            description = "TODO",
            required = False,
            default = None
        )
    ):
        embed = Embed()
        embed.set_author(name=f"{interaction.user.name}'s Hit & Blow Game", icon_url=interaction.user.display_avatar.url)
        embed.description = f"Click the button to guess a number"
        embed.colour = random.choice(main.embed_colours)
        embed.set_footer(text="0 guesses")
        view = HitAndBlowView(interaction, HitAndBlowData(), bet)
        await interaction.response.send_message(embed=embed, view=view)

    #@nextcord.slash_command(name="slots", description="play a nice game of slots", guild_ids=[main.DEVS_SERVER_ID])

def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))