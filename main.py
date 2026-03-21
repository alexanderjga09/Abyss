import os

import discord
import roman
from discord.ext import commands
from dotenv import load_dotenv

import modules.fish as fs
import modules.fishimg as fsi

load_dotenv()


class Client(commands.Bot):
    async def on_ready(self):
        print(f"We have logged in as {self.user}")


intents = discord.Intents.all()
client = Client(intents=intents)

placeholder: str = "https://static.wikitide.net/deepspiritwiki/thumb/4/47/Placeholder.png/250px-Placeholder.png"


def main():
    @client.slash_command(name="fish", description="placeholder")
    async def fish(
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
        try:
            embed = discord.Embed(
                title=f"{fs.Mayus(fish.name)} (${fish.price()}) ({fish.weight}Kg)",
                description=f"**$/hr:** {fish.production(rsl=rsl)['roe_per_hour']} `50%~ {fish.production(rsl=rsl)['roe_per_hour'] / 2}`\n**Kg/hr:** {fish.production(rsl=rsl)['weight_per_hour']} `50%~ {fish.production(rsl=rsl)['weight_per_hour'] / 2}`\n"
                if fish.production(rsl=rsl) is not None
                else "-# Can't do that",
                color=discord.Color.yellow(),
            )
            embed.add_field(
                name="Details:",
                value=f"**Stars:** {((':star: ' * fish.stars) + f'`x{0.25 + (0.25 * fish.stars)}`') if not fish.dead else ':skull: `x0.2`'} | **Rarity:** {fish.rarity} `{fish.production(rsl=rsl)['cycle_time']}m`\n**Mutation:** {fish.mutation} `x{fish.production(rsl=rsl)['mutation']}`",
            )

            embed.set_thumbnail(
                url=fish.thumbnail if not fish.thumbnail == "" else placeholder
            )
            embed.set_image(url=fish.production(rsl=rsl)["chart"])
            embed.set_footer(text=f"Roe Speed Level: {roman.toRoman(rsl)}")

            await interaction.response.send_message(embed=embed)

        except TypeError:
            import json

            with open("data/mutations.json") as f:
                mutations = json.load(f)

            embed = discord.Embed(
                title=f"{fs.Mayus(fish.name)} (${fish.price()}) ({fish.weight}Kg)",
                description=f"**$/hr:** {fish.production(rsl=rsl)['roe_per_hour']} `50%~ {fish.production(rsl=rsl)['roe_per_hour'] / 2}`\n**Kg/hr:** {fish.production(rsl=rsl)['weight_per_hour']} `50%~ {fish.production(rsl=rsl)['weight_per_hour'] / 2}`\n"
                if fish.production(rsl=rsl) is not None
                else "-# Can't do that",
                color=discord.Color.yellow(),
            )
            embed.add_field(
                name="Details:",
                value=f"**Stars:** {((':star: ' * fish.stars) + f'`x{0.25 + (0.25 * fish.stars)}`') if not fish.dead else ':skull: `x0.2`'} | **Rarity:** {fish.rarity}\n**Mutation:** {fish.mutation} `x{mutations[fish.mutation if fish.mutation != '' else 'None']}`",
            )

            embed.set_thumbnail(
                url=fish.thumbnail if not fish.thumbnail == "" else placeholder
            )

            await interaction.response.send_message(embed=embed)

    @client.slash_command(name="fish-img", description="placeholder")
    async def fish_img(
        interaction: discord.Interaction, img: discord.Attachment, rsl: int
    ):
        await interaction.response.defer()

        img_bytes = await img.read()
        fish_instance = fsi.FishImage(img_bytes, rsl)
        resultado = fish_instance.get_fish()

        fish = fs.Fish(
            resultado["name"],
            resultado["weight"],
            resultado["stars"],
            resultado["mutation"],
            False if resultado["stars"] is not bool else True,
        )
        try:
            embed = discord.Embed(
                title=f"{fs.Mayus(fish.name)} (${fish.price()}) ({fish.weight}Kg)",
                description=f"**$/hr:** {fish.production(rsl=rsl)['roe_per_hour']} `50%~ {fish.production(rsl=rsl)['roe_per_hour'] / 2}`\n**Kg/hr:** {fish.production(rsl=rsl)['weight_per_hour']} `50%~ {fish.production(rsl=rsl)['weight_per_hour'] / 2}`\n"
                if fish.production(rsl=rsl) is not None
                else "-# Can't do that",
                color=discord.Color.yellow(),
            )
            embed.add_field(
                name="Details:",
                value=f"**Stars:** {((':star: ' * fish.stars) + f'`x{0.25 + (0.25 * fish.stars)}`') if not fish.dead else ':skull: `x0.2`'} | **Rarity:** {fish.rarity} `{fish.production(rsl=rsl)['cycle_time']}m`\n**Mutation:** {fish.mutation} `x{fish.production(rsl=rsl)['mutation']}`",
            )

            embed.set_thumbnail(
                url=fish.thumbnail if not fish.thumbnail == "" else placeholder
            )
            embed.set_image(url=fish.production(rsl=rsl)["chart"])
            embed.set_footer(text=f"Roe Speed Level: {roman.toRoman(rsl)}")

            await interaction.followup.send(embed=embed)

        except TypeError:
            import json

            with open("data/mutations.json") as f:
                mutations = json.load(f)

            embed = discord.Embed(
                title=f"{fs.Mayus(fish.name)} (${fish.price()}) ({fish.weight}Kg)",
                description=f"**$/hr:** {fish.production(rsl=rsl)['roe_per_hour']} `50%~ {fish.production(rsl=rsl)['roe_per_hour'] / 2}`\n**Kg/hr:** {fish.production(rsl=rsl)['weight_per_hour']} `50%~ {fish.production(rsl=rsl)['weight_per_hour'] / 2}`\n"
                if fish.production(rsl=rsl) is not None
                else "-# Can't do that",
                color=discord.Color.yellow(),
            )
            embed.add_field(
                name="Details:",
                value=f"**Stars:** {((':star: ' * fish.stars) + f'`x{0.25 + (0.25 * fish.stars)}`') if not fish.dead else ':skull: `x0.2`'} | **Rarity:** {fish.rarity}\n**Mutation:** {fish.mutation} `x{mutations[fish.mutation if fish.mutation != '' else 'None']}`",
            )

            embed.set_thumbnail(
                url=fish.thumbnail if not fish.thumbnail == "" else placeholder
            )

            await interaction.followup.send(embed=embed)

    client.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
