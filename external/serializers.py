import filetype
from drf_extra_fields.fields import Base64FileField
from rest_framework.response import Response
from rest_framework.status import *


class CustomBase64FileField(Base64FileField):
    ALLOWED_TYPES = []

    def __init__(self, required=False, allowed_types=None, **kwargs):
        self.ALLOWED_TYPES = allowed_types if allowed_types else [
            'pdf', 'txt', 'xml', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'svg', 'mp3',
            'wav', 'mp4', 'mov', 'avi', 'zip', 'tar', 'gz', 'csv', 'xls', 'xlsx'
        ]
        kwargs['required'] = required
        super().__init__(**kwargs)

    def get_file_extension(self, filename, decoded_file):
        kind = filetype.guess(decoded_file)
        if not kind or kind.extension not in self.ALLOWED_TYPES:
            return Response({'error': 'Given file type is not supported'}, status=HTTP_400_BAD_REQUEST)
        return kind.extension
