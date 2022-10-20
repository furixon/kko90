from django.contrib import admin
from .models import *

from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.


# 사이트 타이틀
admin.site.site_header = "KKO90 - WITHNATURE"
admin.site.site_title = "KKO90 ADMIN"
admin.site.index_title = "KKO90 ADMIN"
admin.empty_value_display = '데이터가 없습니다! ^^;'
admin.empty_value_display = 'DATA NOT FOUND ^^;'

# admin.site.enable_nav_sidebar = False


class KkoMsgResource(resources.ModelResource):

    class Meta:
        model = KkoMsg
        skip_unchanged = True
        report_skipped = False
        exclude = ('id', )
        import_id_fields = ('client_id', 'msg_index')


@admin.register(KkoMsg)
class KkoMsgAdmin(ImportExportModelAdmin):
    list_display = list_display_links = ['agency_name', 'client_name', 'msg_index', 'client_id', 'kko_url', 'request_at', 'send_at', 'result', ]
    resource_classes = [KkoMsgResource]


class AgencyResource(resources.ModelResource):

    class Meta:
        model = Agency


@admin.register(Agency)
class AgencyAdmin(ImportExportModelAdmin):
    list_display = list_display_links = ['agency_name', 'kko_id', 'kko_pass', 'reg_at', 'update_at',]
    resource_classes = [AgencyResource]


class MsgTemplateResource(resources.ModelResource):

    class Meta:
        model = MsgTemplate
        skip_unchanged = True
        report_skipped = False
        exclude = ('id', 'update_at')
        import_id_fields = ('send_type', 'msg_index')


@admin.register(MsgTemplate)
class MsgTemplateAdmin(ImportExportModelAdmin):
    list_display = list_display_links = ['send_type', 'msg_index', 'msg_content', 'update_at', ]
    resource_classes = [MsgTemplateResource]