# serializers.py
from rest_framework import serializers
from .models import Podcast, Episode
from django.contrib.auth.models import User

class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = '__all__'

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'

class UserSubscriptionsSerializer(serializers.ModelSerializer):
    subscriptions = PodcastSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'subscriptions')
