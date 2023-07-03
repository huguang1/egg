# -*- coding: utf-8 -*-
# 18-7-14 下午2:38
# AUTHOR:June
from django.conf.urls import url
from lottery.views import RecordView, MineView, InfoView, LoginView, IndexView
from lottery.tests import TimeVerifyView
urlpatterns = [
    url(r'^$',IndexView.as_view(), name='index'),
    url(r'^lottery/records$', RecordView.as_view(), name='recs'),
    url(r'^lottery/verify$', LoginView.as_view(), name='new'),
    url(r'^lottery/records/mine$', MineView.as_view(), name='mine'),
    url(r'^lottery/info$',InfoView.as_view(), name='info')
    # url(r'^info$', TimeVerifyView.as_view(), name='info')

]
