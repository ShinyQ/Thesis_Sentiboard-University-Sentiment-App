# Generated by Django 3.2.4 on 2022-10-04 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentiment',
            name='created_at',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
