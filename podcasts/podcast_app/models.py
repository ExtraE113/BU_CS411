from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Podcast(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    rss_feed_url = models.URLField()
    category = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='subscriptions')

    def __str__(self):
        return self.title

class Episode(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=200)
    description = models.TextField()
    audio_file = models.FileField(upload_to='podcast_episodes/')
    published_date = models.DateTimeField()
    duration = models.DurationField()
    ad_timestamps = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title 