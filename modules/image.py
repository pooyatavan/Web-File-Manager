from PIL import Image
import os

from modules.config import Config
from modules.tools import GetRootProject
from modules.log import LOG
from modules.strings import Console

BASE_DIR = GetRootProject() + "\\dir"

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
    except Exception as error:
        LOG.warning(Console.CompressError.value.format(error=error))

def create_thumbnail(image_path, thumb_path, size=(int(Config.read()['image']['width']), int(Config.read()['image']['height']))):
    try:
        with Image.open(image_path) as img:
            img.thumbnail(size)
            img.save(thumb_path)
            LOG.info(Console.ConvertThumbnailS.value.format(file=image_path))
    except Exception as error:
        LOG.error(Console.ConvertThumbnailE.value.format(file=error))

def Scan():
    counter = 0
    for root, dirs, files in os.walk(BASE_DIR):
        for file_name in files:
            if "thumb_" not in file_name:
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                    image_path = os.path.join(root, file_name)
                    thumb_path = os.path.join(root, os.path.splitext('thumb_' + file_name)[0] + os.path.splitext(file_name)[1])
                    if not os.path.exists(thumb_path):
                        counter = counter + 1
                        create_thumbnail(image_path, thumb_path)      
    LOG.info(Console.ScanForThumbnail.value.format(counter=counter))