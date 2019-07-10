# Generated by Django 2.1.7 on 2019-06-24 23:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20190623_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='birthday',
        ),
        migrations.AddField(
            model_name='profile',
            name='birth',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(2019), django.core.validators.MinValueValidator(1920)]),
        ),
        migrations.AddField(
            model_name='profile',
            name='religion',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_male',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='likes_iphone',
            field=models.BooleanField(null=True),
        ),
    ]