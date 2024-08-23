from PIL import Image

from modules.config import Config
from modules.tools import GetRootProject
from modules.log import LOG
from modules.strings import Console

def compress_image(file_path, filename):
    try:
        if file_path.replace(GetRootProject(), "") == "\\dir\\":
            with Image.open(file_path + filename) as img:
                img = img.resize((int(Config.read()['image']['width']), int(Config.read()['image']['height'])), Image.LANCZOS).convert('RGB')
                img.save(file_path + "thumb_" + filename, "JPEG", quality=int(Config.read()['image']['quality']))
        else:
            with Image.open(file_path + "\\" + filename) as img:
                img = img.resize((int(Config.read()['image']['width']), int(Config.read()['image']['height'])), Image.LANCZOS).convert('RGB')
                img.save(file_path + "\\" + "thumb_" + filename, "JPEG", quality=int(Config.read()['image']['quality']))
    except:
        LOG.warning(Console.CompressError.value)