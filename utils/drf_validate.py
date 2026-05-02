from typing import List

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.exceptions import ValidationError


def validation_file_size(file: InMemoryUploadedFile, max_size_byte: int) -> None:
    size = file.size
    if size and size > max_size_byte:
        raise ValidationError(F"Размер файла {file.name} больше допустимого")


def validation_type_file(file: InMemoryUploadedFile, files_types: List[str]) -> None:
    file_name = file.name
    file_type = file_name.split(".")[-1]
    if file_type not in files_types:
        raise ValidationError(F"Формат файла {file.name} запрещён к загрузке")
