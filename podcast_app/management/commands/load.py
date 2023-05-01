import requests
import hashlib
import feedparser
import time
from django.core.management import BaseCommand
from podcast_app.models import Podcast, Episode
import datetime
from datetime import timedelta, datetime
import pytz

from config import API_KEY as API_KEY
from config import API_SECRET as API_SECRET

def parse_itunes_duration(duration_string):
    if duration_string is None:
        duration_parts = [0, 0, 0]  # Default value for duration (0 minutes and 0 seconds)
    else:
        duration_parts = list(map(int, duration_string.split(':')))
    if len(duration_parts) == 3:
        hours, minutes, seconds = duration_parts
    elif len(duration_parts) == 2:
        hours = 0
        minutes, seconds = duration_parts
    else:
        hours = 0
        minutes = 0
        seconds = duration_parts[0]

    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def fetch_top_podcasts():
    url = 'https://api.podcastindex.org/api/1.0/podcasts/trending?pretty'
    headers = {
        'X-Auth-Date': str(int(time.time())),
        'User-Agent': 'Podcast_Adblocker'
    }
    params = {
        'count': 5,  
    }

    auth_token = hashlib.sha1((API_KEY + API_SECRET + headers['X-Auth-Date']).encode()).hexdigest()
    headers['X-Auth-Key'] = API_KEY
    headers['Authorization'] = auth_token

    response = requests.get(url, headers=headers, params=params)
    return response.json()['feeds']

class Command(BaseCommand):
    def handle(self, *args, **options):
        podcasts_data = fetch_top_podcasts()

        for podcast_data in podcasts_data:
            title = podcast_data.get('title')
            description = podcast_data.get('description')
            rss_feed_url = podcast_data.get('url')
            cover = podcast_data.get('image', 'artwork')

            podcast, created = Podcast.objects.get_or_create(rss_feed_url=rss_feed_url)
            if created:
                podcast.title = title
                podcast.description = description
                podcast.cover = cover
                podcast.save()
            
            feed = feedparser.parse(rss_feed_url)

            # Iterate through the episodes in the RSS feed
            for entry in feed.entries:
                episode_title = entry.get('title')
                episode_description = entry.get('description', '')
                episode_audio_file = entry.get('enclosures', [{}])[0].get('url', '')
                episode_published_date = datetime.fromtimestamp(
                    time.mktime(entry.get('published_parsed')), tz=pytz.UTC
                )
                episode_time = entry.get('itunes_duration')
                episode_duration = parse_itunes_duration(episode_time)
                

                # Create and save the Episode model instance
                episode = Episode(
                    podcast=podcast,
                    title=episode_title,
                    description=episode_description,
                    audio_file=episode_audio_file,
                    published_date=episode_published_date,
                    duration=episode_duration,
                )
                episode.save()