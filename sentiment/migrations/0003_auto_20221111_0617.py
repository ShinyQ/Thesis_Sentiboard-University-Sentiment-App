# Generated by Django 3.2.4 on 2022-11-11 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0002_sentiment_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentiment',
            name='month',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='sentiment',
            name='year',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
