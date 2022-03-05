from nextcord.ui import Button, View
import nextcord

class TestView(View):
    @nextcord.ui.button(
                label = "End Interaction", 
                style = nextcord.ButtonStyle.red,
                emoji = "⏹️")

    async def button_callback(self, button, interaction):
        button.label = "Interaction ended"
        button.Disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Interaction ended.")