# Generated by Django 2.0.4 on 2018-04-25 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0004_auto_20180425_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='playermatch',
            name='index',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
