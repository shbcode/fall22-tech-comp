from io import BytesIO
from PIL import Image
from django.core.files import File
import re

def compress_image(image, name, target_width=1000):
    name = re.sub(r'[^ \w+]', '', name.replace(" #", "")).replace(" ", "-")
    img = Image.open(image)
    new_height = int(target_width*(float(img.size[1])/float(img.size[0])))
    img = img.resize((target_width, new_height)).convert("RGB")
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=75)
    img_file = File(img_io, name=f"{name}.jpg")
    return img_file
