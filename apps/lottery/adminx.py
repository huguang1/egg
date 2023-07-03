# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from extra_apps import xadmin
from lottery.models import Prize, Rule, Member, Rec, Info,Sysmem
import xlrd
import datetime, pytz
from import_export import resources # 导入excel按钮
from xadmin.plugins.actions import BaseActionView
from xadmin import views
# 创建xadmin的最基本管理器配置，并与view绑定
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True
# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView, BaseSetting)

class MenberResources(resources.ModelResource):
    """会员导入类"""

    class Meta:
        model = Member
        fields = ('id','username', 'score','extra_str')

class RuleResources(resources.ModelResource):
    """规则导入类"""

    class Meta:
        model = Rule
        fields = ('id','username','prize_id')



class Globalsettings(object):

    site_title = '抽奖后台管理系统'
    site_footer = '有限公司'
    # menu_style = 'accordion'
xadmin.site.register(views.CommAdminView,Globalsettings)


class PrizeAdmin(object):
    list_display = ['prize_id','name','probability','is_show']
    search_fields = ['prize_id','name','desc','probability','is_show']
    ordering = ['prize_id']
    list_per_page = 15
    list_editable = ['probability', 'name']
    model_icon = 'fa fa-gift'

class RuleAdmin(object):
    list_display = ['id', 'username','prize_id','is_use','create_time','is_delete']
    search_fields = ['username','prize_id','is_use','is_delete']
    list_filter = ['prize_id','is_delete','create_time']
    ordering = ['use_time']
    list_per_page = 15
    ordering = ['-id']
    import_export_args = {'import_resource_class': RuleResources} # 导入规则
    model_icon = 'fa fa-play'


class MemberAdmin(object):
    list_display = ['id','username','score','create_time','update_time','is_delete']
    search_fields = ['username','score','is_delete']
    list_filter = ['create_time','update_time','is_delete','score']
    ordering = ['-create_time']
    list_per_page = 15
    list_editable = ['score', 'is_delete']
    import_export_args = {'import_resource_class': MenberResources}  #  导入会员
    model_icon = 'fa fa-user'
	

class SendAction(BaseActionView):
    action_name = "send_action"
    description = u'发送所选的 奖品'
    model_perm = 'change'
    def do_action(self, queryset):
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))
        queryset.update(is_sent=True, send_time=now)


class RecAdmin(object):
    list_display = ['id','user','is_sent','prize','send_time','user_ip','way','create_time','update_time','is_delete']
    search_fields = ['user','prize__prize_id','is_sent','way','is_delete']
    list_filter = ['prize','send_time','user_ip','way','create_time','update_time','is_sent','is_delete']
    ordering = ['-create_time']
    list_per_page = 15
    list_editable = ['is_sent','is_delete','send_time']
    # aggregate_fields = {'user':'sum'}
    actions = [SendAction,]
    model_icon = 'fa fa-check-square'


class InfoAdmin(object):
    list_display = ['name', 'is_open', 'errmsg', 'start_time', 'end_time', 'times', 'timee', 'create_time', 'update_time', 'is_delete']
    list_editable = ['is_open', 'is_delete', 'errmsg', 'start_time', 'end_time', 'times', 'timee']
    ordering = ['create_time']
    list_per_page = 10
    model_icon = 'fa fa-calendar'


xadmin.site.register(Prize, PrizeAdmin)
xadmin.site.register(Rule, RuleAdmin)
xadmin.site.register(Member, MemberAdmin)
xadmin.site.register(Rec, RecAdmin)
xadmin.site.register(Info, InfoAdmin)
# xadmin.site.register(Sysmem)






