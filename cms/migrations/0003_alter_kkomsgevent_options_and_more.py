# Generated by Django 4.1.1 on 2023-07-31 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_kkomsgevent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kkomsgevent',
            options={'verbose_name': '이벤트 메시지 요청', 'verbose_name_plural': '이벤트 메시지 요청'},
        ),
        migrations.AlterModelOptions(
            name='publicmsgtemplate',
            options={'verbose_name': '이벤트 메시지 템플릿', 'verbose_name_plural': '이벤트 메시지 템플릿'},
        ),
        migrations.RemoveField(
            model_name='publicmsgtemplate',
            name='end_at',
        ),
        migrations.AlterField(
            model_name='kkomsgevent',
            name='msg_index',
            field=models.CharField(max_length=24, verbose_name='이벤트코드'),
        ),
        migrations.AlterField(
            model_name='kkomsgevent',
            name='request_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='등록일시'),
        ),
        migrations.AlterField(
            model_name='publicmsgtemplate',
            name='msg_index',
            field=models.CharField(max_length=24, verbose_name='코드'),
        ),
        migrations.AlterField(
            model_name='publicmsgtemplate',
            name='start_at',
            field=models.DateTimeField(verbose_name='전송일시'),
        ),
    ]
