import io
import json
import re


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


def Mayus(text: str) -> str:
    return " ".join(map(str.capitalize, text.split(" ")))


def PerHour(mount, cycle_time, rsl=0):
    return (mount / (cycle_time * ((1.0 + (0.05 * rsl)) ** -1))) * 3600


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

    def production(self, rsl: int = 0):
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
                "chart": qc.get_url(),
            }


def extract(txt: str):
    with open("data/prices.json") as f:
        fishes = json.load(f)

    with open("data/mutations.json") as f:
        mutations = json.load(f)

    data = {
        "mutation": "None",
        "name": "None",
        "stars": "None",
        "weight": "None",
    }

    for x in mutations.keys():
        if re.search(x, txt) is not None:
            data["mutation"] = x
            break

    for x in fishes["fishes"].keys():
        if re.search(x, txt) is not None:
            data["name"] = x
            break

    estrellas = {"(x1)": 3, "(x075)": 2, "(x05)": 1, "(x02)": True}

    for x in estrellas.keys():
        if re.search(x, txt) is not None:
            data["stars"] = int(estrellas[x])
            break

    weight_match = re.search(r"(\d+\.?\d*)\s*kg", txt)

    data["weight"] = float(weight_match.group(0)[:-2])

    return data


class FishImage:
    def __init__(self, img_bytes, rsl: int):
        self.img_bytes = io.BytesIO(img_bytes)
        self.rsl = rsl

    def get_fish(self):
        import pytesseract as tss
        from PIL import Image

        tss.pytesseract.tesseract_cmd = r"ocr\tesseract.exe"
        image = Image.open(self.img_bytes).convert("L")

        w, h = image.size
        image = image.resize((w * 4, h * 4), Image.Resampling.LANCZOS)

        fn = lambda x: 255 if x > 70 else 0
        image = image.point(fn, mode="1")

        custom_config = r"--psm 6 --oem 3"

        text = tss.image_to_string(image, config=custom_config)

        return extract(text)
