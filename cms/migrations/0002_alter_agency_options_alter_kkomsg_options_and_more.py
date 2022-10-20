# Generated by Django 4.1.1 on 2022-09-21 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agency',
            options={'verbose_name': '지점', 'verbose_name_plural': '지점'},
        ),
        migrations.AlterModelOptions(
            name='kkomsg',
            options={'verbose_name': '메시지 요청', 'verbose_name_plural': '메시지 요청'},
        ),
        migrations.AlterModelOptions(
            name='msgtemplate',
            options={'verbose_name': '메시지 템플릿', 'verbose_name_plural': '메시지 템플릿'},
        ),
        migrations.AlterField(
            model_name='kkomsg',
            name='result',
            field=models.CharField(blank=True, default='요청', max_length=64, null=True, verbose_name='상태'),
        ),
    ]