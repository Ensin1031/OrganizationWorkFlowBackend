from typing import BinaryIO

from PIL import Image
from django.core.exceptions import ValidationError as DjangoValidationError


def validate_image_size(fieldfile_obj):
    """ Валидатор на размер фотографии. На веб сервере стоит ограничение на 20м"""
    filesize = fieldfile_obj.size
    megabyte_limit = 3.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise DjangoValidationError(f"Максимальный размер файла: {megabyte_limit}MB")


def validate_is_image(image):
    """ Валидатор на формат фотографии. """
    try:
        image_name = image.file.name  # для админки
    except Exception:
        image_name = image.name  # для rest хвоста

    image_format = [image_name.endswith('.svg'),
                    image_name.endswith('.gif'),
                    image_name.endswith('.png'),
                    image_name.endswith('.jpg'),
                    image_name.endswith('.jpeg')]
    if not any(image_format):
        raise DjangoValidationError("Не правильный формат данных. Только SVG, GIF, PNG, JPG, JPEG.")
    return True


def validate_is_image_not_broken(image: BinaryIO):
    """ Валидатор фотографии целостность. """
    try:
        img = Image.open(image)
        img.verify()  # Проверка целостности файла
        return True
    except Exception:
        raise DjangoValidationError("Битый файл")
