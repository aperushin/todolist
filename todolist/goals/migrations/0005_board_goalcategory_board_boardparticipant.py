# Generated by Django 4.2.4 on 2023-08-11 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0004_alter_goal_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(verbose_name='Created')),
                ('updated', models.DateTimeField(verbose_name='Updated')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Deleted')),
            ],
            options={
                'verbose_name': 'Board',
                'verbose_name_plural': 'Boards',
            },
        ),
        migrations.AddField(
            model_name='goalcategory',
            name='board',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='goals.board', verbose_name='Board'),
        ),
        migrations.CreateModel(
            name='BoardParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(verbose_name='Created')),
                ('updated', models.DateTimeField(verbose_name='Updated')),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'Owner'), (2, 'Writer'), (3, 'Reader')], default=1, verbose_name='Role')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='participants', to='goals.board', verbose_name='Board')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='participants', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Participant',
                'verbose_name_plural': 'Participants',
                'unique_together': {('board', 'user')},
            },
        ),
    ]
