# Generated by Django 2.2.7 on 2019-12-04 18:25

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('groupName', models.CharField(max_length=50, verbose_name='Group Name')),
                ('creationDate', models.DateField(default=datetime.datetime.now, verbose_name='Group Creation Date')),
            ],
            options={
                'verbose_name_plural': 'Groups',
            },
        ),
        migrations.CreateModel(
            name='TimeOfJoining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now, verbose_name='Joining Time')),
                ('isAdmin', models.BooleanField(default=False, verbose_name='Admin')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='groups.Groups')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Time of Joining',
            },
        ),
    ]
