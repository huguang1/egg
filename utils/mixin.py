# -*- coding: utf-8 -*-
# 18-7-14 下午6:54
# AUTHOR:June
from django.views.generic import View
from lottery.models import Info

from django.contrib.auth.decorators import login_required


class TimeVerifyView(View):
    Info.objects.filter(is_delete=False).last()
