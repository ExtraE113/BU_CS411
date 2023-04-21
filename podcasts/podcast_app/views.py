from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Podcast, Episode
from .serializers import PodcastSerializer, EpisodeSerializer, UserSubscriptionsSerializer
from django.contrib.auth.models import User
# Create your views here.


class PodcastList(generics.ListAPIView):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer

class EpisodeList(generics.ListAPIView):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer

class UserSubscriptions(generics.RetrieveUpdateAPIView):
    serializer_class = UserSubscriptionsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user 








