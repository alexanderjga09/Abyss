import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import fish as fs

load_dotenv()


class Client(commands.Bot):
    async def on_ready(self):
        print(f"We have logged in as {self.user}")


intents = discord.Intents.all()
client = Client(intents=intents)


def main():
    @client.slash_command(name="info_fish", description="placeholder")
    async def info_fish(
        interaction: discord.Interaction,
        name: str,
        weight: float,
        stars: int,
        mutation: str = "",
        dead: bool = False,
        roe_speed_level: int = 0,
    ):
        fish = fs.Fish(name, weight, stars, mutation, dead)

        embed = discord.Embed(
            title=fish.name,
            description=f"**Price:** ${fish.price()}\n**Weight:** {fish.weight} Kg",
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="Details:",
            value=f"**Stars:** {':star: ' * fish.stars}\n**Rarity:** {fish.rarity}\n**Mutation:** {fish.mutation}\n**Dead:** {fish.dead}",
        )
        embed.add_field(
            name="Production:",
            value=f"**$/hr:** {fish.production(rsl=roe_speed_level)['roe_per_hour']}\n**Kg/hr:** {fish.production(rsl=roe_speed_level)['weight_per_hour']}\n"
            if fish.production(rsl=roe_speed_level) is not None
            else "-# Can't do that",
        )

        await interaction.response.send_message(embed=embed)

    client.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
