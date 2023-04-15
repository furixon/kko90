from django.db import models

# Create your models here.


class KkoMsg(models.Model):
    # msg_id = models.AutoField(primary_key=True)
    agency_name = models.CharField(max_length=128, verbose_name='지점명', blank=True, null=True)
    client_name = models.CharField(max_length=128, verbose_name='고객명', blank=True, null=True)
    msg_index = models.CharField(max_length=24, verbose_name='차수코드')
    client_id = models.CharField(max_length=128, verbose_name='고객번호', blank=True, null=True)
    kko_url = models.CharField(max_length=255, verbose_name='카카오링크')
    request_at = models.DateTimeField(auto_now_add=True, verbose_name='요청일시')
    send_at = models.DateTimeField(verbose_name='업데이트', blank=True, null=True, auto_now=True)
    result = models.CharField(max_length=64, default='요청', verbose_name='상태', blank=True, null=True)

    class Meta:
        verbose_name = '메시지 요청'
        verbose_name_plural = '메시지 요청'

    def __str__(self):
        return str(self.pk)


class Agency(models.Model):
    agency_name = models.CharField(max_length=128, verbose_name='지점명', blank=True, null=True)
    kko_id = models.CharField(max_length=128, verbose_name='카카오 아이디', blank=True, null=True)
    kko_pass = models.CharField(max_length=128, verbose_name='카카오 비번', blank=True, null=True)
    report_url = models.CharField(max_length=256, verbose_name='리포트 수신', blank=True, null=True)
    report_owner_name = models.CharField(max_length=128, verbose_name='인증담당자', blank=True, null=True)
    report_owner_tel = models.CharField(max_length=128, verbose_name='인증담당 연락처', blank=True, null=True)
    reg_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일시')
    update_at = models.DateTimeField(auto_now=True, verbose_name='업데이트')

    class Meta:
        verbose_name = '지점'
        verbose_name_plural = '지점'

    def __str__(self):
        return self.agency_name


class MsgTemplate(models.Model):
    SEND_TYPE = (('A', '공통'), ('B', '지점'), )
    send_type = models.CharField(max_length=2, default='A', choices=SEND_TYPE, verbose_name='전송타입')
    msg_index = models.CharField(max_length=24, verbose_name='차수코드')
    msg_content = models.TextField(blank=True, null=True, verbose_name='메시지')
    img_content = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='이미지')
    link_content = models.URLField(max_length=512, blank=True, null=True, verbose_name='외부링크')
    update_at = models.DateTimeField(auto_now=True, verbose_name='업데이트')

    class Meta:
        verbose_name = '메시지 템플릿'
        verbose_name_plural = '메시지 템플릿'

    def __str__(self):
        return str(self.pk)


class PublicMsgTemplate(models.Model):
    msg_index = models.CharField(max_length=24, verbose_name='차수코드')
    msg_content = models.TextField(blank=True, null=True, verbose_name='메시지')
    img_content = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='이미지')
    link_content = models.URLField(max_length=512, blank=True, null=True, verbose_name='외부링크')
    start_at = models.DateTimeField(verbose_name='시작일')
    end_at = models.DateTimeField(verbose_name='종료일')
    update_at = models.DateTimeField(auto_now=True, verbose_name='업데이트')

    class Meta:
        verbose_name = '부가 메시지 템플릿'
        verbose_name_plural = '부가 메시지 템플릿'

    def __str__(self):
        return str(self.pk)
