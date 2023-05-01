from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Podcast, Episode
from .serializers import PodcastSerializer, EpisodeSerializer, UserSubscriptionsSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
# Create your views here.

class PodcastList(generics.ListAPIView):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
    

class EpisodeList(generics.ListAPIView):
    serializer_class = EpisodeSerializer

    def get_queryset(self):
        podcast_id = self.kwargs['podcast_id']
        get_object_or_404(Podcast, id=podcast_id)
        return Episode.objects.filter(podcast_id=podcast_id)
    
class UserSubscriptions(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSubscriptionsSerializer

    def get_object(self):
        return self.request.user.subscriptions.all()

class SubscribeToPodcast(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, podcast_id):
        podcast = get_object_or_404(Podcast, id=podcast_id)
        podcast.users.add(request.user)
        podcast.save()
        return Response({'status': 'success', 'message': 'Subscribed to podcast.'})

class UnsubscribeFromPodcast(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, podcast_id):
        podcast = get_object_or_404(Podcast, id=podcast_id)
        podcast.users.remove(request.user)
        podcast.save()
        return Response({'status': 'success', 'message': 'Unsubscribed from podcast.'})
