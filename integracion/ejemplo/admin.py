# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Ejemplo
from .models import SensoresClaro


admin.site.register(Ejemplo)
admin.site.register(SensoresClaro)

# Register your models here.
