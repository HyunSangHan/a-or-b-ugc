# Generated by Django 2.1.7 on 2019-05-06 06:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedpage', '0009_auto_20190502_0130'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='hashtag',
            name='feed',
        ),
        migrations.AlterField(
            model_name='feed',
            name='upvote_users',
            field=models.ManyToManyField(blank=True, related_name='upvote_feeds', through='feedpage.Upvote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tagrelation',
            name='feed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedpage.Feed'),
        ),
        migrations.AddField(
            model_name='tagrelation',
            name='hash_tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedpage.HashTag'),
        ),
        migrations.AddField(
            model_name='feed',
            name='matched_tags',
            field=models.ManyToManyField(blank=True, related_name='tagged_feeds', through='feedpage.TagRelation', to='feedpage.HashTag'),
        ),
    ]
