import json


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
                        "$/hr",
                        "PriceRoe(pts)",
                        "Kg/hr(pts)",
                        "Mutation(pts)",
                    ],
                    "datasets": [
                        {
                            "backgroundColor": "rgba(54, 162, 235, 0.5)",
                            "borderColor": "rgb(54, 162, 235)",
                            "data": [
                                pr_hour,
                                price * 50,
                                we_hour * 50,
                                (mutations[self.mutation] * 250)
                                if self.mutation != ""
                                else 50,
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
                },
            }

            return {
                "price_roe": round(price, 0),
                "roe_per_hour": round(pr_hour, 0),
                "roe_per_day": round(pr_hour * 24, 0),
                "weight_roe": round(weight, 2),
                "weight_per_hour": round(we_hour, 2),
                "weight_per_day": round(we_hour * 24, 2),
                "chart": qc.get_url(),
            }
