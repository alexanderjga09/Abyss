import json
import re

with open("data/prices.json") as f:
    FISHES = json.load(f)["fishes"]

with open("data/mutations.json") as f:
    MUTATIONS = json.load(f)

ESTRELLAS = {
    "(x1)": 3,
    "(01)": 3,
    "(x075)": 2,
    "(x0.75)": 2,
    "(x07)": 2,
    "(x05)": 1,
    "(x0.5)": 1,
    "(x02)": True,
    "(x0.2)": True,
}

UNREADABLES = {
    "x6.66": "Shadow",
    "x2.8": "Amber",
}


STAR_PATTERNS = [(re.compile(k), v) for k, v in ESTRELLAS.items()]
UNREADABLE_PATTERNS = [(re.compile(k), v) for k, v in UNREADABLES.items()]
MUTATION_PATTERNS = [(re.compile(k), k) for k in MUTATIONS.keys()]
FISH_PATTERNS = [(re.compile(name), name) for name in FISHES.keys()]


def extract(txt: str):
    data: dict = {"mutation": "None", "name": "None", "stars": "None", "weight": "None"}

    for pattern, name in MUTATION_PATTERNS:
        if pattern.search(txt):
            data["mutation"] = name
            break
    else:
        for pattern, name in UNREADABLE_PATTERNS:
            if pattern.search(txt):
                data["mutation"] = name
                break

    for pattern, name in FISH_PATTERNS:
        if pattern.search(txt):
            data["name"] = name
            break

    for pattern, stars in STAR_PATTERNS:
        if pattern.search(txt):
            data["stars"] = stars
            break

    weight_match = re.search(r"(\d+\.?\d*)\s*kg", txt)
    if weight_match:
        data["weight"] = float(weight_match.group(1))

    return data
