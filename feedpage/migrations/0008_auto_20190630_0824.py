# Generated by Django 2.1.7 on 2019-06-29 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedpage', '0007_auto_20190630_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedcomment',
            name='content',
            field=models.CharField(max_length=70),
        ),
    ]