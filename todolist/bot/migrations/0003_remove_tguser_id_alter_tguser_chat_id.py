# Generated by Django 4.2.4 on 2023-08-21 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_rename_tg_chat_id_tguser_chat_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tguser',
            name='id',
        ),
        migrations.AlterField(
            model_name='tguser',
            name='chat_id',
            field=models.BigIntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Telegram chat id'),
        ),
    ]
