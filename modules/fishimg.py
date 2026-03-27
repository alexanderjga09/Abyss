import io

import cv2
import numpy as np
import pytesseract as tss
from PIL import Image

from .func.Autocorrector import Text, cut_
from .func.Corrector_w import corrects_weights
from .func.Extract import extract

tss.pytesseract.tesseract_cmd = r"ocr\tesseract.exe"

try:
    with open("dict.txt", "r", encoding="utf-8") as f:
        _EXPECTED_WORDS = [line.strip() for line in f]
except FileNotFoundError:
    _EXPECTED_WORDS = []


class FishImage:
    def __init__(self, img_bytes, save_debug: bool = False):
        self.img_bytes = io.BytesIO(img_bytes)
        self.save_debug = save_debug

    def get_fish(self):
        image = Image.open(self.img_bytes).convert("L")

        w, h = image.size
        image = image.resize((w * 6, h * 6), Image.Resampling.LANCZOS)

        img_np = np.array(image)

        _, binary = cv2.threshold(img_np, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((3, 3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        if np.sum(binary == 0) > np.sum(binary == 255):
            binary = cv2.bitwise_not(binary)

        if self.save_debug:
            cv2.imwrite("debug.png", binary)

        pil_image = Image.fromarray(binary)

        custom_config = r"--psm 6 --oem 3 --user-words dict.txt"

        text = tss.image_to_string(pil_image, config=custom_config)

        text_c = Text(text).correct(_EXPECTED_WORDS, cutoff=0.6)
        text_c = corrects_weights(text_c)

        return extract(cut_(text_c))
