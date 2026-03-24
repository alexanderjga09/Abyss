import difflib
import re


class Text:
    def __init__(self, text: str):
        self.text = text

    def correct(self, expected_words: list[str], cutoff=0.8):
        text_words = self.text.split()
        corrected = []
        for word in text_words:
            if word in expected_words:
                corrected.append(word)
            else:
                matches = difflib.get_close_matches(
                    word, expected_words, n=1, cutoff=cutoff
                )
                if matches:
                    corrected.append(matches[0])
                else:
                    corrected.append(word)
        return " ".join(corrected)

    def cut_(self, txt: str):
        return re.sub(
            (
                r"\b(Common|Uncommon|Rare|Epic|Legendary|Mythical)\b.*?(\d+(?:\.\d+)?\s?kg)"
            ),
            r"\1 \2",
            txt,
            flags=re.IGNORECASE,
        )
