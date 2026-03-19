import os

import discord
import roman
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
        name=discord.Option(str, "The name of the fish"),
        weight=discord.Option(float, "The weight of the fish"),
        stars=discord.Option(int, "The number of stars the fish has"),
        mutation=discord.Option(str, "The mutation of the fish", default=""),
        dead: bool = False,
    ):
        fish = fs.Fish(
            name,
            round(weight if "," in str(weight) else (weight * 0.1), 1),
            stars,
            mutation,
            dead,
        )

        embed = discord.Embed(
            title=fish.name,
            description=f"**Price:** ${fish.price()}\n**Weight:** {fish.weight} Kg",
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="Details:",
            value=f"**Stars:** {((':star: ' * fish.stars) + f'`x{0.25 + (0.25 * fish.stars)}`') if not fish.dead else ':skull: `x0.2`'} | **Rarity:** {fish.rarity} `{fish.production()['cycle_time']}m`\n**Mutation:** {fish.mutation} `x{fish.production()['mutation']}`",
        )
        embed.set_thumbnail(url=fish.thumbnail)

        await interaction.response.send_message(embed=embed)

    @client.slash_command(name="prod_fish", description="placeholder")
    async def prod_fish(
        interaction: discord.Interaction,
        name=discord.Option(str, "The name of the fish"),
        weight=discord.Option(float, "The weight of the fish"),
        stars=discord.Option(int, "The number of stars the fish has"),
        mutation=discord.Option(str, "The mutation of the fish", default=""),
        dead: bool = False,
        rsl: int = 0,
    ):
        fish = fs.Fish(
            name,
            round(weight if "," in str(weight) else (weight * 0.1), 1),
            stars,
            mutation,
            dead,
        )
        embed = discord.Embed(
            title=f"{fish.name} (${fish.price()})",
            description=f"**$/hr:** {fish.production(rsl=rsl)['roe_per_hour']}\n**Kg/hr:** {fish.production(rsl=rsl)['weight_per_hour']}\n"
            if fish.production(rsl=rsl) is not None
            else "-# Can't do that",
            color=discord.Color.yellow(),
        )
        embed.add_field(
            name="Details:",
            value=f"**Stars:** {((':star: ' * fish.stars) + f'`x{0.25 + (0.25 * fish.stars)}`') if not fish.dead else ':skull: `x0.2`'} | **Rarity:** {fish.rarity} `{fish.production(rsl=rsl)['cycle_time']}m`\n**Mutation:** {fish.mutation} `x{fish.production(rsl=rsl)['mutation']}`",
        )

        embed.set_thumbnail(url=fish.thumbnail)
        embed.set_image(url=fish.production(rsl=rsl)["chart"])
        embed.set_footer(text=f"Roe Speed Level: {roman.toRoman(rsl)}")

        await interaction.response.send_message(embed=embed)

    client.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
