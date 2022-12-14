from django.db import models

class Sentiment(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField(unique=True)
    preprocessing = models.TextField()
    label = models.SmallIntegerField()
    month = models.TextField(default=None, null=True)
    year = models.IntegerField(default=None, null=True)
    created_at = models.DateField(default=None, blank=True, null=True)
