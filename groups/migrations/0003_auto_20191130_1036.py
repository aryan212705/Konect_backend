# Generated by Django 2.2.7 on 2019-11-30 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_auto_20191130_1027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groups',
            options={'verbose_name_plural': 'Groups'},
        ),
        migrations.AlterModelOptions(
            name='timeofjoining',
            options={'verbose_name_plural': 'Time of Joining'},
        ),
        migrations.AddField(
            model_name='timeofjoining',
            name='isAdmin',
            field=models.BooleanField(default=False),
        ),
    ]
