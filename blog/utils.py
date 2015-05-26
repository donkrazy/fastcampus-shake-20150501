# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import uuid
from django.utils import timezone
from django.utils.encoding import force_text, smart_text


def random_name_upload_to(model_instance, filename):
    app_label = model_instance.__class__._meta.app_label
    model_cls_name = model_instance.__class__.__name__.lower()
    dirpath_format = app_label + '/' + model_cls_name + '/%Y/%m/%d'  # "모델클래스명/년/월/일"
    dirpath = os.path.normpath(force_text(timezone.now().strftime(smart_text(dirpath_format))))
    random_name = uuid.uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()
    return dirpath + '/' + random_name + extension

