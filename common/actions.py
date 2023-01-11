from django.core.files.base import ContentFile
import base64
from django.utils import timezone

from common.models import Image
from logisticproject.exceptions import BadeRequestException


class SaveImage:
    def __init__(self, serializer, author):
        self._serializer = serializer
        self._author = author

    def save(self):
        images = list()
        for obj in self._serializer.validated_data:
            image = obj.get('image')
            extensions = obj.get('extensions')
            try:
                file = ContentFile(base64.b64decode(image), name=f'image-{timezone.now()}.{extensions}')
            except:
                raise BadeRequestException(message='Invalid image', code='invalid')
            image_model = Image.objects.create(file=file, author=self._author)
            images.append(image_model.id)
        return images