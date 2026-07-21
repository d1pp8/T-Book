from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


def make_image(name='image.jpg',content_type='image/jpeg'):
    buffer = BytesIO()

    Image.new('RGB', (100, 100)).save(buffer, format='JPEG')

    return SimpleUploadedFile(
        name=name,
        content=buffer.getvalue(),
        content_type=content_type,
    )