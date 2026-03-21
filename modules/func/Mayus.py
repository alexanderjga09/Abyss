def Mayus(text: str) -> str:
    return " ".join(map(str.capitalize, text.split(" ")))
