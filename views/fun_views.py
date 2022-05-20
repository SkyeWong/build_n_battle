import os
import nextcord
import random
import main
import math 
from main import bot
from datetime import datetime
from nextcord.ext import commands, tasks
from nextcord import Embed, SelectOption, Interaction
from nextcord.ui import Button, View, button, Modal, TextInput, select, Select
import database as db
from typing import Optional
from functions.users import Users

class Analysis(View):
                
    def __init__(self, interaction: Interaction, result, most, least):
        super().__init__(timeout=180)
        self.interaction = interaction
        self.most = most
        self.least = least
        self.result = result

    @button(
        label = "Show Analysis", 
        style = nextcord.ButtonStyle.blurple, 
        emoji = "📊"
    )
    async def show_analysis(self, button, interaction):
        embed = Embed()
        msg = "```md\n"
        msg += "# Analysis:\n"
        msg += "\t- <MOST>:\n"
        for i in self.most:
            msg += f"\t\t* [{self.result.count(str(i))}]({i}s)\n"
        msg += "\t- <LEAST>:\n"
        for i in self.least:
            msg += f"\t\t* [{self.result.count(str(i))}]({i}s)\n"
        msg += "> great, isn't it? took SkyeWong#8577 2 days to make this!\n"
        msg += "```"
        embed.description = msg
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True
        await self.interaction.edit_original_message(view=self)

class HitAndBlowData():
    
    def __init__(self):
        self.ans = []
        for i in range(4):
            self.ans.append(str(random.randint(0, 9)))
        self.tries = []
        self.correct = False
class HitAndBlowView(View):

    def __init__(self, slash_interaction: Interaction, data_class, bet: int):
        super().__init__(timeout=1800)
        self.slash_interaction = slash_interaction
        self.data_class = data_class
        self.bet = bet

    @button(
        label = "GUESS!",
        emoji = "🔢",
        style = nextcord.ButtonStyle.blurple
    )
    async def show_modal(self, button, interaction: Interaction):
        await interaction.response.send_modal(HitAndBlowModal(self, self.slash_interaction, interaction, self.data_class, self.bet))

    @button(
        label = "INFO",
        emoji = "ℹ️",
        style = nextcord.ButtonStyle.grey
    )
    async def info(self, button, interaction: Interaction):
        points = {
            "A fun code breaking game also known as _Cows and Bulls_ or _Pigs and Bulls_": "",
            "The board game _Mastermind_ and the popular online word game _Wordle_ originated from this!": "",
            "How to play:": {
                "①": "I am gonna choose a **random four-digit** number (0-9)",
                "②": "You have to try to **guess** it, that's hard, right? So I will give you some hints.",
                "③": "If the matching digits are in their **right positions** → **HIT**",
                "④": "If they are in **different positions** → **BLOW**",
                "⑤": "EG:\n⠀⠀my num:   **`5968`**\n\⠀⠀your num: **`5683`**\n\⠀⠀`1` HIT `(5)` and `2` BLOWS `(6, 8)`"
            },
            "Get it? GOOD LUCK!": ""
        }
        msg = ""
        for point in points:
            msg += f"\n**`➼`** {point}"
            if points[point] != "":
                for subpoint in points[point]:
                    msg += f"\n⠀`{subpoint}` {points[point][subpoint]}"
        embed = Embed()
        embed.set_author(
            name = "HIT & BLOW INFO",
            icon_url = bot.user.display_avatar.url
        )
        embed.description = msg
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True
        slash_msg = await self.slash_interaction.original_message()
        msg_embed = slash_msg.embeds[0]
        msg_embed.colour = 0xde2f41
        users = Users(self.slash_interaction.user)
        msg_embed.set_author(name=f"{self.slash_interaction.user.name}'s lost Hit & Blow Game", icon_url=self.slash_interaction.user.display_avatar.url)
        msg_embed.description = f"Unfortunately, you didn't make a guess for a bit too long...⌛\nThe correct number is - `{''.join(self.data_class.ans)}`"
        if self.bet != 0:
            msg_embed.description += f"\nYou lost your ${self.bet} bet."
            users.modify_gold(0 - self.bet)
        await self.slash_interaction.edit_original_message(embed=msg_embed, view=self)
        
    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.slash_interaction.user:
            await interaction.response.send_message(f"This is not for you, sorry. Use `/{self.slash_interaction.application_command.name}` to play the game.", ephemeral=True)
            return False
        else:
            return True

class HitAndBlowModal(Modal):

    def __init__(self, btn_class: View, slash_interaction: Interaction, btn_interaction: Interaction, data_class, bet: int):
        super().__init__(
            title = "Hit & Blow",
            timeout = None
        )
        self.btn_class = btn_class
        self.slash_interaction = slash_interaction
        self.btn_interaction = btn_interaction
        self.data_class = data_class
        self.bet = bet
        self.num = TextInput(
            label = "Enter a four-digit number",
            min_length = 4,
            max_length = 4
        )
        self.add_item(self.num)

    async def callback(self, interaction: Interaction):
        slash_msg = await self.slash_interaction.original_message()
        msg_embed = slash_msg.embeds[0]
        msg_embed = main.delete_field(msg_embed, "⚠️ ERROR!")
        if self.num.value.isnumeric():
            tries = self.data_class.tries
            tries.append(self.num.value)
            guesses_field_value = ""
            for i in range(len(tries)):
                hits = 0
                blows = 0
                ans = self.data_class.ans
                guess = tries[i]
                for x in range(4):
                    if ans[x] == guess[x]:
                        hits += 1
                        if hits == 4:
                            self.data_class.correct = True
                    for y in range(4):
                        if ans[y] == guess[x] and ans[x] != guess[x] and ans[y] != guess[y]:
                            blows += 1
                            break
                guesses_field_value += f"\n`{i + 1}` ﹕ `{tries[i]}`〢`{hits}` H & `{blows}` B"
            msg_embed.clear_fields()
            msg_embed.add_field(name="GUESSES", value=guesses_field_value)    
            msg_embed.set_footer(text=f"{len(tries)} guesses")
            bet_msg = f" ● betting {self.bet}" if self.bet != 0 else ""
            msg_embed.set_footer(text=f"{len(tries)} guesses{bet_msg}")
            if len(tries) > 15 or self.data_class.correct == True:
                btn_class = self.btn_class
                users = Users(self.slash_interaction.user)
                for i in btn_class.children:
                    i.disabled = True
                await self.slash_interaction.edit_original_message(view=btn_class)
                if len(tries) > 15:
                    msg_embed.colour = 0xde2f41
                    msg_embed.set_author(name=f"{interaction.user.name}'s lost Hit & Blow Game", icon_url=interaction.user.display_avatar.url)
                    msg_embed.description = f"Sadly, you didn't guess the number in 15 tries 😥\nThe correct number is - `{''.join(self.data_class.ans)}`"
                    if self.bet != 0:
                        msg_embed.description += f"\nYou lost your ${self.bet} bet."
                        users.modify_gold(0 - self.bet)
                if self.data_class.correct == True:
                    msg_embed.colour = 0x77b255
                    msg_embed.set_author(name=f"{interaction.user.name}'s won Hit & Blow Game", icon_url=interaction.user.display_avatar.url)
                    msg_embed.description = f"YAY you actually got it! I knew you could 😉\nThe correct number is - `{''.join(self.data_class.ans)}`"
                    if self.bet != 0:
                        won_bet = self.bet
                        reduction = 0
                        if len(tries) > 5:
                            reduction = (len(tries) - 5) * 8
                        won_bet = round(self.bet * (100 - reduction) / 100)
                        msg_embed.description += f"\nYou won ${won_bet}!"
                        users.modify_gold(won_bet)
        else:
            msg_embed.add_field(name="⚠️ ERROR!", value="The inputted value is not a four-digit number", inline=False)
        await self.slash_interaction.edit_original_message(embed=msg_embed)

class HappyBirthdayView(View):
    
    def __init__(self, slash_interaction: Interaction, questions: list[dict]):
        super().__init__(timeout=180)
        self.questions = questions
        self.question = self.get_random_question()
        self.slash_interaction = slash_interaction
        answer_select = [i for i in self.children if i.custom_id == "answer"][0]
        answer_select.options = self._get_select_options()
        self.stopped = None

    def get_random_question(self):
        return random.choice(self.questions)

    def get_question_embed(self):
        question = self.question
        embed = Embed()
        description = question["question"]
        for i in question["answers"]:
            description += f"\n{i}, {'correct' if question['answers'][i] else 'wrong'}"
        embed.description = description
        embed.colour = random.choice(main.embed_colours)
        return embed

    def _get_select_options(self) -> list[SelectOption]:
        options = []
        question = self.question
        answers = question["answers"]
        for option in answers:
            options.append(
                SelectOption(
                    label = option
                )
            )
        return options
    
    @tasks.loop(seconds=10.0)
    async def spam_dm(self):
        user = self.slash_interaction.user
        view = View()
        stop_btn = Button(label="STOP")
        stop_btn.callback = self.stop_spam_dm
        view.add_item(stop_btn)
        for i in range(6):
            await user.send(f"Happy Birthday, {user.mention}", view=view)

    async def stop_spam_dm(self, interaction: Interaction):
        if not self.stopped:
            self.spam_dm.cancel()
            self.stopped = True
        else:
            await interaction.send("i've already stopped didn't i")
    
    @select(placeholder="What's your answer?", options=[], custom_id="answer")
    async def user_answer(self, select: Select, interaction: Interaction):
        answers = self.question["answers"]
        if answers[select.values[0]] == True :
            await interaction.send("You are right!", ephemeral=True)
            await self.on_timeout()  # disable buttons
            if not self.stopped:
                self.spam_dm.start()
                self.stopped = False
        else:
            await interaction.send("you are wrong!", ephemeral=True)
            self.question = self.get_random_question()
            answer_select = [i for i in self.children if i.custom_id == "answer"][0]
            answer_select.options = self._get_select_options()
            await self.slash_interaction.edit_original_message(embed=self.get_question_embed(), view=self)

    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True
        await self.slash_interaction.edit_original_message(view=self)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.slash_interaction.user:
            await interaction.response.send_message(f"This is not for you, sorry.\nUse `/{self.slash_interaction.application_command}`", ephemeral=True)
            return False
        else:
            return True