from django.shortcuts import render
import bisect, random, datetime, pytz
from lottery.models import Rec, Rule, Prize, Info, Member
from django.views.generic import View
from django.http.response import JsonResponse
from django.core.paginator import Paginator
from datetime import timedelta


class IndexView(View):
    def get(self, request):
        info = Info.objects.filter(is_delete=False).last()
        if info:
            text = info.text
        else:
            text = ''
        return render(request,'index.html', {"text": text})


class RecordView(View):
    """记录视图"""
    def post(self,request):
        records = Rec.objects.filter(is_delete=False).order_by('-create_time')[0:30]
        data = [{
            'user': rec.user[:2]+'***',
            'prize': rec.prize.name,
            'date': rec.create_time
                } for rec in records]
        return JsonResponse(data, safe=False)


class MineView(View):
    """查询视图"""
    def get(self, request):
        querycode = request.GET.get('querycode')
        pIndex = request.GET.get('p')
        size = request.GET.get('size')
        lottery_record = Rec.objects.filter(user=querycode).order_by('-create_time')
        if lottery_record is None:
            data1 = {'count': 0, 'data': []}
            return JsonResponse(data1, safe=False)
        count = lottery_record.count()
        # 如果当前没有传递页码信息，则认为是第一页，这样写是为了请求第一页时可以不写页码
        if pIndex == '':
            pIndex = '1'
        # 通过url匹配的参数都是字符串类型，转换成int类型
        try:
            pIndex = int(pIndex)
        except Exception as e:
            # 参数错误
            data1 = {'count': 0, 'data': []}
            return JsonResponse(data1, safe=False)

        try:
            size = int(size)
        except Exception as e:
            # 参数错误
            data1 = {'count': 0, 'data': []}
            return JsonResponse(data1, safe=False)
        # 将地区信息按一页size条进行分页
        p = Paginator(lottery_record, int(size))
        # 获取第pIndex页的数据
        lottery_record = p.page(pIndex)
        # 组织信息
        list_query = []
        for user_obj in lottery_record:
            rec_obj = {
                "user_name": user_obj.user,
                "prize_name": user_obj.prize.name,
                "is_send": user_obj.is_sent,
                "win_time": (user_obj.create_time + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            }
            list_query.append(rec_obj)
        data1 = {"count":count, "data": list_query}
        return JsonResponse(data1,safe=False)


class LoginView(View):
    """登录视图"""
    def post(self, request):
        try:
            symbol = request.POST.get('bonuscode')
        except Exception as e:
            data={
                'stat': '-1'
            }
            return JsonResponse(data, safe=False)
        # 用户为空返回用户登录
        if symbol == '':
            data = {
                'stat': '-1',
                'msg': 'NO USER MESSAGE'
            }
            return JsonResponse(data, safe=False)
        # 获取用户查询集
        try:
            users = Member.objects.filter(username=symbol, is_delete=False)
        except Exception as e:
            data = {
                'stat': '-2',
                'msg': 'errors in query'
            }
            return JsonResponse(data, safe=False)
        # 查询抽奖机会
        if users.exists():
            times = users.values('score').first().get('score')
            if times < 1:
                data = {
                    'stat': '-2',
                    'msg': 'no changes'
                }
                return JsonResponse(data, safe=False)
            else:
                data = {
                    'stat': '0',
                    'score': times
                }
                return JsonResponse(data, safe=False)
        else:
            data = {
                'stat': '-2'
            }
            return JsonResponse(data, safe=False)


class InfoView(View):
    """活动抽奖视图"""
    def post(self, request):
        # 时间校验
        info = Info.objects.filter(is_delete=False).last()
        if info.is_open == False:
            return JsonResponse({'stat':'5','msg':info.errmsg}, safe=False)
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))
        moment = datetime.datetime.now().time()

        # 与活动时间进行比较
        s_time = Info.objects.filter(is_delete=False).first().start_time
        e_time = Info.objects.filter(is_delete=False).first().end_time
        times = Info.objects.filter(is_delete=False).first().times
        timee = Info.objects.filter(is_delete=False).first().timee
        if (times <= moment <= timee) and s_time <= now <= e_time:
            # 获取ip信息
            if 'HTTP_X_FORWARDED_FOR' in request.META.values():
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            # 获取请求信息
            try:
                symbol = request.POST.get('bonuscode')
            except Exception as e:
                data = {
                    'stat': '5'
                }
                return JsonResponse(data, safe=False)
            # 用户为空返回用户登录
            if symbol == '':
                data = {
                    'stat': '-1',
                    'msg': 'NO USER MESSAGE'
                }
                return JsonResponse(data, safe=False)
            # 获取用户查询集
            try:
                users = Member.objects.filter(username=symbol, is_delete=False)
            except Exception as e:
                data = {
                    'stat': '5',
                    'msg': 'errors in query'
                }
                return JsonResponse(data, safe=False)
            # 查询抽奖机会
            if users.exists():
                times = users.values('score').first().get('score')
                if times > 0:
                    rules = Rule.objects.filter(is_delete=False, username=symbol, is_use=False).order_by('create_time')
                    if rules.exists():
                        pzid = rules.values('prize_id').first().get('prize_id')
                        rule_prize = Prize.objects.filter(prize_id=pzid).first()
                        # 次数减少
                        Member.objects.filter(username=symbol, is_delete=False).update(score=times - 1)
                        # 生成抽奖记录
                        Rec.objects.create(user=users.first().username, prize=rule_prize, user_ip=ip, way='内定抽奖')
                        # 逻辑删除内定记录
                        rule = rules.first()
                        rule.is_use = True
                        rule.save()
                        data = {
                            'stat': '0',
                            'pId': pzid,
                            'msg': rule_prize.name
                        }
                        return JsonResponse(data, safe=False)
                    else:
                        # 自然抽奖
                        prizes = Prize.objects.filter(is_show=True).order_by('prize_id')
                        mkarr = [int(prize.probability * 100) for prize in prizes]
                        sernum = WeightRandom(mkarr).result()
                        prizenum = prizes[sernum]
                        # 次数减少
                        Member.objects.filter(username=symbol, is_delete=False).update(score=times - 1)
                        # 生成抽奖记录
                        Rec.objects.create(user=users.first().username, prize=prizenum, user_ip=ip)
                        data = {
                            'stat': '0',
                            'pId': sernum+1,
                            'msg': prizenum.name
                        }
                        return JsonResponse(data, safe=False)



                else:
                    data = {
                        'stat': '-3',
                        'msg': 'NO CHANGES'
                    }
                    return JsonResponse(data, safe=False)
            else:
                data = {'stat': '-1',}
                return JsonResponse(data)
        else:
            data = {
                    'stat': '5',
                    'msg': info.errmsg
                }
            return JsonResponse(data, safe=False)


class WeightRandom:
    """抽奖算法"""
    def __init__(self, items):
        weights = items
        self.total = sum(weights)
        self.acc = list(self.accumulate(weights))

    @staticmethod
    def accumulate(weights):  # 累和.如accumulate([10,40,50])->[10,50,100]
        cur = 0
        for w in weights:
            cur = cur + w
            yield cur

    def result(self):
        return bisect.bisect_right(self.acc, random.uniform(0, self.total))
