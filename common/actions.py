import base64

from django.core.files.base import ContentFile
from django.utils import timezone

from common.models import File
from logisticproject.exceptions import BadeRequestException


class SaveFile:
    def __init__(self, serializer, author):
        self._serializer = serializer
        self._author = author

    def save(self):
        files = list()
        for obj in self._serializer.validated_data:
            file = obj.get('file')
            extensions = obj.get('extensions')
            try:
                file = ContentFile(base64.b64decode(file), name=f'file-{timezone.now()}.{extensions}')
            except:
                raise BadeRequestException(message='Invalid file', code='invalid')
            file_model = File.objects.create(file=file, author=self._author)
            files.append(file_model.id)
        return files
