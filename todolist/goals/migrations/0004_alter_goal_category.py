# Generated by Django 4.2.4 on 2023-08-10 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0003_goalcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='goals', to='goals.goalcategory', verbose_name='Category'),
        ),
    ]
