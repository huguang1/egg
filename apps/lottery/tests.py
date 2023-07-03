from django.test import TestCase

# Create your tests here.
from lottery.models import Info
from django.views.generic import View
from django.http.response import JsonResponse
import datetime
import pytz


class TimeVerifyView(View):
    def post(self, re):
        info = Info.objects.filter(is_delete=False).last()
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))
        moment = datetime.datetime.now().time()

        # 与活动时间进行比较
        # s_time = Info.objects.all().values('start_time').first().get('start_time')
        s_time = Info.objects.filter(is_delete=False).first().start_time
        print('s_time', s_time)
        e_time = Info.objects.all().values('end_time').first().get('end_time')
        times = Info.objects.all().values('times').first().get('times')
        timee = Info.objects.all().values('timee').first().get('timee')
        ntimes = Info.objects.all().values('ntimes').first().get('ntimes')
        ntimee = Info.objects.all().values('ntimee').first().get('ntimee')
        print(s_time, e_time, times, timee, ntimes, ntimee, moment)
        if (times <= moment <= timee or ntimes <= moment <= ntimee) and s_time <= now <= e_time:
            return JsonResponse({'stat': '-1'}, safe=False)
        else:
            data = {
                    'stat': '5',
                    'msg': info.errmsg
                }
            return JsonResponse(data, safe=False)
