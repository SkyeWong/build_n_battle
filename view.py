from nextcord.ui import Button, View
import nextcord
from typing import Optional
import random
from cogs.build_and_battle import Users
class EndInteraction(View):
    @nextcord.ui.button(label = "End Interaction", style = nextcord.ButtonStyle.red, emoji = "⏹️")
    async def button_callback(self, button, interaction):
        button.label = "Interaction ended"
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Interaction ended.")

class generate(View):

    def __init__(self, ctx, timeout: Optional[float] = 30):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    @nextcord.ui.button(label = "Generate gold!", style = nextcord.ButtonStyle.grey, emoji = "🪙")
    async def gold_generate(self, button, interaction):
        profile = list(users.get_user_profile(self.ctx.author))
        profile[1] += 500
        profile = users.update_user_profile(self.ctx.author, profile)
        button.label = "Gold optained!"
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Something appears in front of you. You pick it up and be **really** suprised that it's some gold COINS!", ephemeral=True)

    @nextcord.ui.button(label = "Generate XP!", style = nextcord.ButtonStyle.grey, emoji = "📚")
    async def xp_generate(self, button, interaction):
        profile = list(users.get_user_profile(self.ctx.author))
        profile[2] += random.choice(range(6))
        profile = users.update_user_profile(self.ctx.author, profile)
        button.label = "No more books..."
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("You take your time and read a book, and learnt something new!", ephemeral=True)