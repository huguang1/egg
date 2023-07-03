from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel
# Create your models here.


class Prize(models.Model):
    """礼品模型类"""
    prize_id = models.IntegerField(default=None, verbose_name='礼品编号')
    name = models.CharField(max_length=150, verbose_name='礼品名称')
    desc = models.CharField(max_length=250, default='', verbose_name='中奖描述')
    probability = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='中奖概率（0.001%）', null=True)
    is_show = models.BooleanField(default=1, verbose_name='列表显示')

    class Meta:
        verbose_name = '奖品管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Rule(BaseModel):
    """内定规则"""
    username = models.CharField(max_length=150, default='', verbose_name='会员账号')
    prize_id = models.IntegerField(default=0, verbose_name='中奖礼品')
    is_use = models.BooleanField(default=False, verbose_name='是否使用')

    class Meta:
        verbose_name = '内定规则'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.username)


class Member(BaseModel):
    """抽奖会员"""
    username = models.CharField(max_length=150, verbose_name='会员账号')
    score = models.IntegerField(default=0, verbose_name='抽奖次数')
    extra_int = models.IntegerField('备用数字', default=0)
    extra_str = models.CharField('备用文字', max_length=255, default=None)

    class Meta:
        verbose_name = '抽奖会员'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.username)


class Rec(BaseModel):
    user = models.CharField('用户', max_length=150)
    prize = models.ForeignKey(Prize, verbose_name='奖品', on_delete=models.PROTECT)
    send_time = models.DateTimeField(verbose_name='发送时间', null=True, default=None)
    is_sent = models.BooleanField(default=False, verbose_name='是否发送')
    user_ip = models.GenericIPAddressField(verbose_name='抽奖IP')
    way = models.CharField(max_length=100, default='自然抽奖', verbose_name='抽奖方式')


    class Meta:
        verbose_name = '抽奖记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


class Info(BaseModel):
    name = models.CharField(max_length=100, verbose_name='活动名称')
    is_open = models.BooleanField(default=False, verbose_name='是否启用')
    errmsg = models.CharField(max_length=100, verbose_name='关闭提示')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    times = models.TimeField(verbose_name='每日起')
    timee = models.TimeField(verbose_name='每日止')
    text = models.CharField('备用文本', max_length=256)

    class Meta:
        verbose_name = '活动设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Sysmem(AbstractUser):
    nickname = models.CharField(max_length=100, verbose_name='姓名')

    class Meta:
        verbose_name = '系统管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
