# Generated by Django 2.1.7 on 2019-06-21 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20190621_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]