import os

from PIL import Image

from tinder import settings


def watermark_photo(image_path):
    """
    Накладывает водяной знак на фото
    """
    base_image = Image.open(image_path)
    watermark = Image.open('static/main/images/water_mark.png')
    width, height = base_image.size

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, (30, 30), mask=watermark)
    transparent = transparent.convert('RGB')

    image_path = os.path.join(settings.MEDIA_ROOT, image_path)
    transparent.save(image_path)
