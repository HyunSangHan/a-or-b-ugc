# Generated by Django 2.1.7 on 2019-05-01 16:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feedpage', '0004_hashtag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='feed',
            name='report',
        ),
        migrations.RemoveField(
            model_name='feed',
            name='upvote_a',
        ),
        migrations.RemoveField(
            model_name='feed',
            name='upvote_b',
        ),
        migrations.RemoveField(
            model_name='feedcomment',
            name='about_a',
        ),
        migrations.AddField(
            model_name='report',
            name='feed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedpage.Feed'),
        ),
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
