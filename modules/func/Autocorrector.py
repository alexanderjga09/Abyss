import difflib


def correct_text(text: str, expected_words: list[str], cutoff=0.8):
    text_words = text.split()
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
