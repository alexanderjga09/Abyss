import json
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
    with open("data/prices.json") as f:
        prices = json.load(f)

    with open("data/mutations.json") as f:
        mutations = json.load(f)

    with open("data/race.json") as f:
        race_json = json.load(f)

    async def get_fish_names(ctx: discord.AutocompleteContext):
        all_fishes = prices["fishes"].keys()
        return [f for f in all_fishes if ctx.value.lower() in f.lower()]

    async def get_mutations(ctx: discord.AutocompleteContext):
        all_mutations = mutations.keys()
        return [m for m in all_mutations if ctx.value.lower() in m.lower()]

    @client.slash_command(name="fish", description="placeholder")
    async def fish(
        interaction: discord.Interaction,
        name: str = discord.Option(
            description="The name of the fish",
            autocomplete=get_fish_names,
        ),
        weight=discord.Option(float, description="The weight of the fish"),
        stars: int = discord.Option(
            description="The number of stars the fish has",
            choices=[
                discord.OptionChoice(name="⭐ ⭐ ⭐", value="3"),
                discord.OptionChoice(name="⭐ ⭐", value="2"),
                discord.OptionChoice(name="⭐", value="1"),
            ],
        ),
        mutation: str = discord.Option(
            description="The mutation of the fish",
            autocomplete=get_mutations,
            default="None",
        ),
        dead: bool = False,
        rsl: int = 0,
        race=discord.Option(
            str,
            description="Your race",
            choices=[
                discord.OptionChoice(name=race_name, value=race_name)
                for race_name in race_json.keys()
            ],
            default=1,
        ),
        cash: float = 0.0,
        food: int = discord.Option(
            description="The food the fish has",
            choices=[
                discord.OptionChoice(name="Star Feed", value="8"),
                discord.OptionChoice(name="Octupus Feed", value="6"),
                discord.OptionChoice(name="Shrimp Feed", value="4"),
                discord.OptionChoice(name="Worm Feed", value="3"),
                discord.OptionChoice(name="Fish Feed", value="2"),
                discord.OptionChoice(name="Algae Feed", value="1"),
            ],
            default=0,
        ),
    ):
        fish = fs.Fish(
            name,
            round(weight if "," in str(weight) else (float(weight) * 0.1), 1),
            int(stars),
            mutation,
            dead,
        )

        cash = round(cash if "," in str(cash) else (float(cash) * 0.1), 1)

        try:
            roe_per_hour = fish.production(rsl=rsl, food=int(food))["roe_per_hour"]

            RoePerHour = (
                f"**$/hr:** {roe_per_hour} `50%~ {round((roe_per_hour / 2), 0)}`"
                if roe_per_hour is not None
                else None
            )
            KgPerHour = (
                f"**Kg/hr:** {(weight_ := fish.production(rsl=rsl, food=int(food))['weight_per_hour'])} `50%~ {round((weight_ / 2), 1)}`"
                if fish.production(rsl=rsl, food=int(food)) is not None
                else None
            )

            with_race_ = fish.production(rsl=rsl, race=race, food=int(food))
            Race = (
                f"\n**With Race:** {round(roe_ := roe_per_hour * with_race_['with_race'], 0)} `50%~ {round((roe_ / 2), 0)}`"
                if with_race_ is not None
                else None
            )
            Cash = (
                f"\n**With Cash:** {round(cash_ := roe_per_hour * (with_race_['with_race'] + (cash * 0.01)), 0)} `50%~ {round((cash_ / 2), 0)}`"
                if with_race_ is not None
                else None
            )
        except Exception:
            pass

        try:
            embed = discord.Embed(
                title=f"{fs.Mayus(fish.name)} (${fish.price()}) ({fish.weight}Kg)",
                description=f"{RoePerHour}\n{KgPerHour}\n{(Race if race != 1 else '')}{Cash if cash != 0.0 else ''}"
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
            embed.set_image(url=fish.production(rsl=rsl, food=int(food))["chart"])

            RSL = (
                f"Roe Speed Level: {roman.toRoman(rsl)}"
                if roman.toRoman(rsl) != "N"
                else ""
            )
            RACE = f"Race: {race}" if race != 1 else ""
            CASH = f"Cash: {str(cash) + '%'}" if cash != 0.0 else ""
            FOOD = f"Food: +{5 * int(food)}%" if food != 0 else ""
            footer = " | ".join([x for x in [RSL, RACE, CASH, FOOD] if x != ""])
            embed.set_footer(text=footer)

            await interaction.response.send_message(embed=embed)

        except TypeError:
            import json

            with open("data/mutations.json") as f:
                mutations = json.load(f)

            embed = discord.Embed(
                title=f"{fs.Mayus(fish.name)} (${fish.price()}) ({fish.weight}Kg)",
                description=""
                if fish.production(rsl=rsl) is not None
                else "-# Can't do that"
                if race is int
                else f"**With Race:** ${round(fish.price() * (race_json[race] if race != 1 else 1), 0)}\n**With Cash:** ${round(fish.price() * ((race_json[race] if race != 1 else 1) + (cash * 0.01)), 0)}",
                color=discord.Color.yellow(),
            )
            embed.add_field(
                name="Details:",
                value=f"**Stars:** {((':star: ' * fish.stars) + f'`x{0.25 + (0.25 * fish.stars)}`') if not fish.dead else ':skull: `x0.2`'} | **Rarity:** {fish.rarity}\n**Mutation:** {fish.mutation} `x{mutations[fish.mutation if fish.mutation != '' else 'None']}`",
            )

            embed.set_thumbnail(
                url=fish.thumbnail if not fish.thumbnail == "" else placeholder
            )

            RACE = f"Race: {race}" if race != 1 else ""
            CASH = f"Cash: {str(cash) + '%'}" if cash != 0.0 else ""
            footer = " | ".join([x for x in [RACE, CASH] if x != ""])
            embed.set_footer(text=footer)

            await interaction.response.send_message(embed=embed)

    @client.slash_command(name="fish-img", description="placeholder")
    async def fish_img(
        interaction: discord.Interaction,
        img: discord.Attachment,
        rsl: int = 0,
        race=discord.Option(
            str,
            description="Your race",
            choices=[
                discord.OptionChoice(name=race_name, value=race_name)
                for race_name in race_json.keys()
            ],
            default=1,
        ),
        cash: float = 0.0,
        food: int = discord.Option(
            description="The food the fish has",
            choices=[
                discord.OptionChoice(name="Star Feed", value="8"),
                discord.OptionChoice(name="Octupus Feed", value="6"),
                discord.OptionChoice(name="Shrimp Feed", value="4"),
                discord.OptionChoice(name="Worm Feed", value="3"),
                discord.OptionChoice(name="Fish Feed", value="2"),
                discord.OptionChoice(name="Algae Feed", value="1"),
            ],
            default=0,
        ),
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

        cash = round(cash if "," in str(cash) else (float(cash) * 0.1), 1)

        try:
            roe_per_hour = fish.production(rsl=rsl, food=int(food))["roe_per_hour"]

            RoePerHour = (
                f"**$/hr:** {roe_per_hour} `50%~ {round((roe_per_hour / 2), 0)}`"
                if roe_per_hour is not None
                else None
            )
            KgPerHour = (
                f"**Kg/hr:** {(weight_ := fish.production(rsl=rsl, food=int(food))['weight_per_hour'])} `50%~ {round((weight_ / 2), 1)}`"
                if fish.production(rsl=rsl, food=int(food)) is not None
                else None
            )

            with_race_ = fish.production(rsl=rsl, race=race, food=int(food))

            Race = (
                f"\n**With Race:** ${round(roe_ := roe_per_hour * with_race_['with_race'], 0)} `50%~ {round((roe_ / 2), 0)}`"
                if with_race_ is not None
                else None
            )
            Cash = (
                f"\n**With Cash:** ${round(cash_ := roe_per_hour * (with_race_['with_race'] + (cash * 0.01)), 0)} `50%~ {round((cash_ / 2), 0)}`"
                if with_race_ is not None
                else None
            )
        except Exception:
            pass

        try:
            embed = discord.Embed(
                title=f"{fs.Mayus(fish.name)} (${fish.price()}) ({fish.weight}Kg)",
                description=f"{RoePerHour}\n{KgPerHour}\n{(Race if race != 1 else '')}{Cash if cash != 0.0 else ''}"
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
            embed.set_image(url=fish.production(rsl=rsl, food=int(food))["chart"])

            RSL = (
                f"Roe Speed Level: {roman.toRoman(rsl)}"
                if roman.toRoman(rsl) != "N"
                else ""
            )
            RACE = f"Race: {race}" if race != 1 else ""
            CASH = f"Cash: {str(cash) + '%'}" if cash != 0.0 else ""
            FOOD = f"Food: +{5 * int(food)}%" if food != 0 else ""
            footer = " | ".join([x for x in [RSL, RACE, CASH, FOOD] if x != ""])
            embed.set_footer(text=footer)

            await interaction.followup.send(embed=embed)

        except TypeError:
            import json

            with open("data/mutations.json") as f:
                mutations = json.load(f)

            embed = discord.Embed(
                title=f"{fs.Mayus(fish.name)} (${fish.price()}) ({fish.weight}Kg)",
                description=""
                if fish.production(rsl=rsl) is not None
                else "-# Can't do that"
                if race is int
                else f"**With Race:** ${round(fish.price() * (race_json[race] if race != 1 else 1), 0)}\n**With Cash:** ${round(fish.price() * ((race_json[race] if race != 1 else 1) + (cash * 0.01)), 0)}",
                color=discord.Color.yellow(),
            )
            embed.add_field(
                name="Details:",
                value=f"**Stars:** {((':star: ' * fish.stars) + f'`x{0.25 + (0.25 * fish.stars)}`') if not fish.dead else ':skull: `x0.2`'} | **Rarity:** {fish.rarity}\n**Mutation:** {fish.mutation} `x{mutations[fish.mutation if fish.mutation != '' else 'None']}`",
            )

            embed.set_thumbnail(
                url=fish.thumbnail if not fish.thumbnail == "" else placeholder
            )

            RACE = f"Race: {race}" if race != 1 else ""
            CASH = f"Cash: {str(cash) + '%'}" if cash != 0.0 else ""
            footer = " | ".join([x for x in [RACE, CASH] if x != ""])
            embed.set_footer(text=footer)

            await interaction.followup.send(embed=embed)

    client.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
