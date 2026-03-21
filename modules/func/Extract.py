import json
import re


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

    for x, y in mutations.items():
        if re.search(x, txt) is not None:
            data["mutation"] = x
            break

        if re.search(("x" + str(y)), txt) is not None and data["mutation"] == "None":
            data["mutation"] = x
            break

    for x in fishes["fishes"].keys():
        if re.search(x, txt) is not None:
            data["name"] = x
            break

    estrellas = {
        "(x1)": 3,
        "(x075)": 2,
        "(x0.75)": 2,
        "(x05)": 1,
        "(x0.5)": 1,
        "(x02)": True,
        "(x0.2)": True,
    }

    for x in estrellas.keys():
        if re.search(x, txt) is not None:
            data["stars"] = int(estrellas[x])
            break

    weight_match = re.search(r"(\d+\.?\d*)\s*kg", txt)

    data["weight"] = float(weight_match.group(0)[:-2])

    return data
