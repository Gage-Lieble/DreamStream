from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

def image_restrictions(image):
    image_width, image_height = get_image_dimensions(image)
    if image_width / image_height != 1:
        raise ValidationError('Sorry but your image must be a square.') 