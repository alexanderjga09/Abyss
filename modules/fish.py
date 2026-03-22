import json

from .func.Mayus import Mayus
from .func.PerHour import PerHour
from .func.Ranks import KgRoe, Mph, Mut, PriceRoe


class Fish:
    def __init__(
        self,
        name: str,
        weight: float,
        stars: int,
        mutation: str = "None",
        dead: bool = False,
    ):
        self.name = Mayus(name)
        self.weight = weight
        self.stars = stars if "Meat" not in self.name and "Head" not in self.name else 3

        with open("data/prices.json") as f:
            prices = json.load(f)

        self.rarity = prices["fishes"][self.name]["rarity"]
        self.thumbnail = prices["fishes"][self.name]["thumbnail"]
        self.mutation = mutation.capitalize()
        self.dead = dead

    def price(self) -> int:
        value = {3: 1.0, 2: 0.75, 1: 0.5}

        with open("data/prices.json") as f:
            prices = json.load(f)

        with open("data/mutations.json") as f:
            mutations = json.load(f)

        return int(
            (
                prices["fishes"][self.name]["price"]
                * self.weight
                * (value[self.stars] if not self.dead else 0.2)
            )
            * (mutations[self.mutation] if self.mutation != "" else 1.0)
        )

    def production(self, rsl: int = 0, race=1):
        cycle_time = {
            "Common": 60,
            "Uncommon": 120,
            "Rare": 240,
            "Epic": 420,
            "Legendary": 600,
        }

        with open("data/prices.json") as f:
            fishes = json.load(f)

        with open("data/mutations.json") as f:
            mutations = json.load(f)

        if "Meat" not in self.name and "Head" not in self.name:
            price = self.price() * (0.01 if self.mutation != "" else 0.02)
            weight = self.weight * 0.02

            pr_hour = PerHour(
                price, cycle_time[fishes["fishes"][self.name]["rarity"]], rsl
            )
            we_hour = PerHour(
                weight, cycle_time[fishes["fishes"][self.name]["rarity"]], rsl
            )

            from quickchart import QuickChart

            qc = QuickChart()
            qc.width = 500
            qc.height = 300
            qc.version = "3"

            # Config can be set as a string or as a nested dict
            qc.config = {
                "type": "radar",
                "data": {
                    "labels": [
                        f"$/hr | Rank: {Mph(pr_hour)[1]}",
                        f"PriceRoe\nRank: {PriceRoe(price)[1]}",
                        f"Kg/hr | Rank: {KgRoe(we_hour)[1]}",
                        f"Mutation\nRank: {Mut((mutations[self.mutation]) if self.mutation != '' else 0)[1]}",
                    ],
                    "datasets": [
                        {
                            "backgroundColor": "rgba(54, 162, 235, 0.5)",
                            "borderColor": "rgb(54, 162, 235)",
                            "data": [
                                Mph(pr_hour)[0],
                                PriceRoe(price)[0],
                                KgRoe(int(round(we_hour, 0)))[0],
                                Mut(
                                    (mutations[self.mutation])
                                    if self.mutation != ""
                                    else 0
                                )[0],
                            ],
                            "label": f"{self.name} (Stats)",
                        },
                    ],
                },
                "options": {
                    "spanGaps": False,
                    "elements": {
                        "line": {
                            "tension": 0.000001,
                        },
                    },
                    "scales": {
                        "r": {
                            "min": 0,  # Valor mínimo
                            "max": 5,  # Valor máximo fijo
                            "ticks": {
                                "display": False  # Oculta los números del eje
                            },
                            "grid": {"circular": True},
                        }
                    },
                },
            }

            with open("data/race.json", "r") as f:
                race_json = json.load(f)

            return {
                "price_roe": round(price, 0),
                "cycle_time": int(
                    cycle_time[fishes["fishes"][self.name]["rarity"]] / 60
                ),
                "mutation": (mutations[self.mutation]) if self.mutation != "" else 1.0,
                "roe_per_hour": round(pr_hour, 0),
                "roe_per_day": round(pr_hour * 24, 0),
                "weight_roe": round(weight, 2),
                "weight_per_hour": round(we_hour, 2),
                "weight_per_day": round(we_hour * 24, 2),
                "with_race": (race if race == 1 else race_json[race]),
                "chart": qc.get_url(),
            }
