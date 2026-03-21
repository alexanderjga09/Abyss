import io

from func.Extract import extract


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
