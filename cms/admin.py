from django.contrib import admin
from .models import *

from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.


# 사이트 타이틀
admin.site.site_header = "KKO90 - WITHNATURAL"
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

    search_fields = ['agency_name', 'client_name', 'client_id']
    list_filter = ['agency_name', 'result']
    actions = ['set_status_complete', 'delete_selected_item']

    def set_status_complete(self, request, queryset):
        queryset.all().update(result='전송완료')

        self.message_user(request, '### 상태변경 완료')
    set_status_complete.short_description = '[0] 상태변경 - 전송완료'

    def delete_selected_item(self, request, queryset):
        queryset.all().delete()

        self.message_user(request, '### Items are deleted')
    delete_selected_item.short_description = '[1] Delete items'


class AgencyResource(resources.ModelResource):

    class Meta:
        model = Agency
        skip_unchanged = True
        report_skipped = False
        exclude = ('id', 'reg_at', 'update_at')
        import_id_fields = ('agency_name', )


@admin.register(Agency)
class AgencyAdmin(ImportExportModelAdmin):
    list_display = list_display_links = ['agency_name', 'kko_id', 'kko_pass', 'report_owner_name', 'report_owner_tel', 'report_url']
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
    list_display = list_display_links = ['send_type', 'msg_index', 'msg_content', 'img_content', 'link_content', 'update_at', ]
    resource_classes = [MsgTemplateResource]


class PublicMsgTemplateResource(resources.ModelResource):

    class Meta:
        model = PublicMsgTemplate
        skip_unchanged = True
        report_skipped = False
        exclude = ('id', 'update_at')
        import_id_fields = ('send_type', 'msg_index')


@admin.register(PublicMsgTemplate)
class MsgTemplateAdmin(ImportExportModelAdmin):
    list_display = list_display_links = ['msg_index', 'msg_content', 'img_content', 'link_content', 'start_at', 'end_at', 'update_at', ]
    resource_classes = [PublicMsgTemplateResource]