# Generated by Django 4.1.1 on 2022-09-21 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_remove_kkomsg_id_kkomsg_msg_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kkomsg',
            name='msg_id',
        ),
        migrations.AddField(
            model_name='kkomsg',
            name='id',
            field=models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]