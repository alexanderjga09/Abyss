import json


def Mph(mph):
    if mph >= 4000:
        return (5, "S")
    if mph >= 3200:
        return (4, "A")
    if mph >= 2400:
        return (3, "B")
    if mph >= 1600:
        return (2, "C")
    if mph >= 800:
        return (1, "D")
    if mph >= 0:
        return (0, "E")


def PriceRoe(pr):
    if pr >= 400:
        return (5, "S")
    if pr >= 320:
        return (4, "A")
    if pr >= 240:
        return (3, "B")
    if pr >= 160:
        return (2, "C")
    if pr >= 80:
        return (1, "D")
    if pr >= 0:
        return (0, "E")


def KgRoe(kr):
    if kr >= 40:
        return (0, "E")
    if kr >= 32:
        return (1, "D")
    if kr >= 24:
        return (2, "C")
    if kr >= 16:
        return (3, "B")
    if kr >= 8:
        return (4, "A")
    if kr >= 0:
        return (5, "S")


def Mut(pr):
    if pr >= 8.5:
        return (5, "S")
    if pr >= 6.8:
        return (4, "A")
    if pr >= 5.1:
        return (3, "B")
    if pr >= 3.4:
        return (2, "C")
    if pr >= 1.7:
        return (1, "D")
    if pr >= 0:
        return (0, "E")


class Fish:
    def __init__(
        self,
        name: str,
        weight: float,
        stars: int,
        mutation: str = "",
        dead: bool = False,
    ):
        self.name = name.capitalize()
        self.weight = weight
        self.stars = stars

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

    def production(self, rsl: int = 0):
        cycle_time = {"Common": 1, "Uncommon": 2, "Rare": 4, "Epic": 7, "Legendary": 10}

        with open("data/prices.json") as f:
            fishes = json.load(f)

        with open("data/mutations.json") as f:
            mutations = json.load(f)

        if "meat" not in self.name and "head" not in self.name:
            price = self.price() * (0.01 if self.mutation != "" else 0.02)
            pr_hour = (
                price
                / (
                    cycle_time[fishes["fishes"][self.name]["rarity"]]
                    * (1.0 - (0.05 * rsl))
                )
            ) * 60

            weight = self.weight * 0.02

            we_hour = (
                weight
                / (
                    cycle_time[fishes["fishes"][self.name]["rarity"]]
                    * (1.0 - (0.05 * rsl))
                )
            ) * 60

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
                            "label": "Stats",
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

            return {
                "price_roe": round(price, 0),
                "cycle_time": cycle_time[fishes["fishes"][self.name]["rarity"]],
                "mutation": (mutations[self.mutation]) if self.mutation != "" else 1.0,
                "roe_per_hour": round(pr_hour, 0),
                "roe_per_day": round(pr_hour * 24, 0),
                "weight_roe": round(weight, 2),
                "weight_per_hour": round(we_hour, 2),
                "weight_per_day": round(we_hour * 24, 2),
                "chart": qc.get_url(),
            }
