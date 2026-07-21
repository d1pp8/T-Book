import pytest
from django.conf import settings

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError

from apps.media.validators import MediaValidator

from apps.media.tests.helper import make_image


def test_validate_valid_image():
    uploaded_file = make_image()
    MediaValidator.validate(uploaded_file)


def test_validate_image_size():
    uploaded_file = make_image()
    uploaded_file.size = settings.MEDIA_MAX_UPLOAD_SIZE + 1
    with pytest.raises(ValidationError, match='Image size exceeds the maximum allowed size.'):
        MediaValidator.validate(uploaded_file)


def test_validate_extension():
    uploaded_file = make_image(name='image.exe')
    with pytest.raises(ValidationError, match='Unsupported file extension.'):
        MediaValidator.validate(uploaded_file)


def test_validate_content_type():
    uploaded_file = make_image(content_type='application/pdf')
    with pytest.raises(ValidationError, match='Unsupported MIME type.'):
        MediaValidator.validate(uploaded_file)


def test_validate_corrupted_image():
    uploaded_file = SimpleUploadedFile(
        name='image.jpg',
        content=b'This is not an image',
        content_type='image/jpeg',
    )

    with pytest.raises(ValidationError, match='Uploaded file is not a valid image.'):
        MediaValidator.validate(uploaded_file)