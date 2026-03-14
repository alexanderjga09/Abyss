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
    @client.slash_command(name="info fish", description="placeholder")
    async def info_fish(
        interaction: discord.Interaction,
        fish_name: str,
        weight: float,
        stars: int,
        mutation: str = "",
        dead: bool = False,
    ):
        fish = fs.Fish(fish_name, weight, stars, mutation, dead)

        embed = discord.Embed(
            title=fish_name,
            description=f"Price: {fish.price()}\nWeight: {weight} Kg\nStars: {stars}\nMutation: {mutation}\nDead: {dead}",
        )

        await interaction.response.send_message(embed=embed)

    client.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
