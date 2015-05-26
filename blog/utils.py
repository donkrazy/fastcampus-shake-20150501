# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import random
import string
from django.utils import timezone
from django.utils.encoding import force_text, smart_text


RANDOM_SAMPLE = string.ascii_letters + string.digits

def random_name_upload_to(model_instance, filename):
    model_cls_name = model_instance.__class__.__name__.lower()
    dirpath_format = model_cls_name + '/%Y/%m/%d/%H%M'  # "모델클래스명/년/월/일/시분"
    dirpath = os.path.normpath(force_text(timezone.now().strftime(smart_text(dirpath_format))))
    random_name = ''.join(random.sample(RANDOM_SAMPLE, 10))
    extension = os.path.splitext(filename)[-1].lower()
    return dirpath + '_' + random_name + extension

