from django.contrib import admin
from .models import *
# Register your models here.


# 사이트 타이틀
admin.site.site_header = "KKO90 - WITHNATURE"
admin.site.site_title = "KKO90 ADMIN"
admin.site.index_title = "KKO90 ADMIN"
admin.empty_value_display = '데이터가 없습니다! ^^;'
admin.empty_value_display = 'DATA NOT FOUND ^^;'

# admin.site.enable_nav_sidebar = False


@admin.register(KkoMsg)
class KkoMsgAdmin(admin.ModelAdmin):
    list_display = list_display_links = ['agency_name', 'client_name', 'msg_index', 'client_id', 'kko_url', 'request_at', 'send_at', 'result', ]


@admin.register(Agency)
class Agency(admin.ModelAdmin):
    list_display = list_display_links = ['agency_name', 'kko_id', 'kko_pass', 'reg_at', 'update_at',]


@admin.register(MsgTemplate)
class MsgTemplate(admin.ModelAdmin):
    list_display = list_display_links = ['send_type', 'msg_index', 'msg_content', 'update_at', ]

