from io import BytesIO

from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError, ImageOps


ALLOWED_IMAGE_FORMATS = {
    'JPEG': 'jpg',
    'PNG': 'png',
    'WEBP': 'webp',
}
MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAX_IMAGE_DIMENSION = 3000
THUMBNAIL_SIZE = (480, 480)


def validate_uploaded_image(uploaded_file):
    if uploaded_file.size > MAX_IMAGE_SIZE:
        raise ValidationError('File too large. Max size is 5MB.')

    try:
        raw_bytes = uploaded_file.read()
        uploaded_file.seek(0)
        image = Image.open(BytesIO(raw_bytes))
        original_format = image.format
        image.verify()
        image = Image.open(BytesIO(raw_bytes))
        image = ImageOps.exif_transpose(image)
    except (UnidentifiedImageError, OSError, ValueError):
        uploaded_file.seek(0)
        raise ValidationError('Invalid or corrupted image file.')

    if original_format not in ALLOWED_IMAGE_FORMATS:
        uploaded_file.seek(0)
        raise ValidationError('Unsupported file type. Allowed: jpg, png, webp.')

    if image.width > MAX_IMAGE_DIMENSION or image.height > MAX_IMAGE_DIMENSION:
        uploaded_file.seek(0)
        raise ValidationError('Image dimensions must not exceed 3000x3000.')

    uploaded_file.seek(0)
    return image


def build_thumbnail(uploaded_file, source_name):
    uploaded_file.seek(0)
    image = Image.open(uploaded_file)
    image = ImageOps.exif_transpose(image)
    image.thumbnail(THUMBNAIL_SIZE)

    if image.mode not in ('RGB', 'RGBA'):
        image = image.convert('RGB')
    elif image.mode == 'RGBA':
        image = image.convert('RGB')

    output = BytesIO()
    image.save(output, format='WEBP', quality=82, optimize=True)
    thumb_name = f"{source_name.rsplit('.', 1)[0]}_thumb.webp"
    return ContentFile(output.getvalue(), name=thumb_name)
