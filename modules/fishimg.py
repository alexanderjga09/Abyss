import io
import re

from .func.Autocorrector import correct_text
from .func.Extract import extract


class FishImage:
    def __init__(self, img_bytes, rsl: int):
        self.img_bytes = io.BytesIO(img_bytes)
        self.rsl = rsl

    def get_fish(self):
        import cv2
        import numpy as np
        import pytesseract as tss
        from PIL import Image

        tss.pytesseract.tesseract_cmd = r"ocr\tesseract.exe"
        image = Image.open(self.img_bytes).convert("L")

        w, h = image.size
        image = image.resize((w * 4, h * 4), Image.Resampling.LANCZOS)

        img_np = np.array(image)

        _, binary = cv2.threshold(img_np, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        kernel = np.ones((3, 3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        if np.sum(binary == 0) > np.sum(binary == 255):
            binary = cv2.bitwise_not(binary)

        image = Image.fromarray(binary)
        image.save("debug.png")

        custom_config = r"--psm 6 --oem 3 --user-words dict.txt"

        text = tss.image_to_string(image, config=custom_config)

        with open("dict.txt", "r") as f:
            expected_words = [line.strip() for line in f]

        text = correct_text(text, expected_words, cutoff=0.75)
        patron = (
            r"\b(Common|Uncommon|Rare|Epic|Legendary|Mythical)\b.*?(\d+(?:\.\d+)?\s?kg)"
        )

        text = re.sub(r"\bTIL(\d*kg)\b", r"111.\1", text)  # PARCHE

        return extract(re.sub(patron, r"\1 \2", text))
