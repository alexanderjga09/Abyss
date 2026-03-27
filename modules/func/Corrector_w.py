import re


def corrects_weights(texto: str) -> str:
    patron = re.compile(r"\b([\w\.]+kg)\b", re.IGNORECASE)

    def _replace(match):
        weight = match.group(1).lower()

        weight = re.sub(r"til(\d+kg)", r"111.\1", weight)
        weight = re.sub(r"(\d+(?:\.\d+)?)k9\b", r"\1kg", weight)
        weight = re.sub(r"(\d+(?:\.\d+)?)k\b", r"\1kg", weight)

        substitutions = {
            "s": "5",
            "o": "0",
            "i": "1",
            "l": "1",
            "h": "1",
            "t": "1",
            "n": "1",
            "z": "2",
            "b": "8",
            "g": "g",
        }
        for bad, good in substitutions.items():
            weight = weight.replace(bad, good)

        weight = re.sub(r"\b(\d+)(\d)kg\b", r"\1.\2kg", weight)

        weight = re.sub(r"\.\.", ".", weight)
        weight = re.sub(r"\s+kg", "kg", weight)

        return weight

    return re.sub(patron, _replace, texto)
