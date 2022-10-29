from base64 import b64decode
from io import BytesIO
from random import choice

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from emoji import emojize
from PIL import Image
from telegram import ReplyKeyboardMarkup

import settings
from db import db, get_random_pic


def create_pic_from_bynary():
    bynary, file_name = get_random_pic(db)
    pic = BytesIO(b64decode(bynary))
    image = Image.open(pic)
    image.save(file_name)

    return file_name


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Отправить мемас', 'Получить мемас'],
        ['Подписаться', 'Отписаться'],
        ['Пройти опрос']
    ])


def has_oblect_on_images(file_name, object_name):
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key {settings.CLARIFAI_API_KEY}'),)

    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)

    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=image))
        ])

    response = app.PostModelOutputs(request, metadata=metadata)
    return check_responce_for_object(response, object_name=object_name)


def check_responce_for_object(response, object_name):
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == object_name and concept.value >= 0.9:
                return True
    else:
        print(f"Ошибка распознавания: {response.outputs[0].status.details}")

    return False


def random_emoji():
    emoji = emojize(choice(settings.USER_EMOJI), language='alias')

    return emoji
