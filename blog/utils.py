# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import uuid
try:
    from io import BytesIO as StringIO # python 3
except ImportError:
    from StringIO import StringIO  # python 2
from contextlib import contextmanager
from PIL import Image
from django.utils import six, timezone
from django.utils.encoding import force_text, smart_text


def random_name_upload_to(model_instance, filename):
    app_label = model_instance.__class__._meta.app_label
    model_cls_name = model_instance.__class__.__name__.lower()
    dirpath_format = app_label + '/' + model_cls_name + '/%Y/%m/%d'  # "모델클래스명/년/월/일"
    dirpath = os.path.normpath(force_text(timezone.now().strftime(smart_text(dirpath_format))))
    random_name = uuid.uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()
    return dirpath + '/' + random_name + extension


@contextmanager
def pil_image(input_f, quality=80):
    if isinstance(input_f, six.string_types):
        filename = input_f
    elif hasattr(input_f, 'name'):
        filename = input_f.name
    else:
        filename = 'noname.png'

    extension = os.path.splitext(filename)[-1].lower()
    try:
        format = {
            '.jpg': 'jpeg',
            '.jepg': 'jpeg',
            '.png': 'png',
            '.gif': 'gif',
        }[extension]
    except KeyError:
        format = 'png'

    image = Image.open(input_f)
    output_f = StringIO()
    yield image, output_f
    image.save(output_f, format=format, quality=quality)
    output_f.seek(0)


def thumbnail(input_f, width, height, quality=80):
    with pil_image(input_f, quality) as (image, output_f):
        image.thumbnail((width, height), Image.ANTIALIAS)
        return output_f

