# Generated by Django 2.1.7 on 2019-05-01 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedpage', '0005_auto_20190502_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='reported',
            field=models.BooleanField(null=True),
        ),
    ]
