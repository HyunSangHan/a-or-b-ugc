# Generated by Django 2.1.7 on 2019-06-29 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedpage', '0005_auto_20190630_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedcomment',
            name='content',
            field=models.CharField(max_length=65),
        ),
    ]