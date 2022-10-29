from base64 import b64decode
from io import BytesIO

from PIL import Image

from db import db, get_random_pic


def create_pic_from_bynary():
    bynary, file_name = get_random_pic(db)
    pic = BytesIO(b64decode(bynary))
    image = Image.open(pic)
    image.save(file_name)

    return file_name
