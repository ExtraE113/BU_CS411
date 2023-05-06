from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Podcast, Episode
from .serializers import PodcastSerializer, EpisodeSerializer, UserSubscriptionsSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from google.oauth2 import id_token
from google.auth.transport import requests


def verify_google_token(token) -> bool:
	CLIENT_ID = '708378597417-g4gp2dmet2rarqs4bb6djof4e3kfnu72.apps.googleusercontent.com'

	try:
		idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

		if 'accounts.google.com' in idinfo['iss']:
			return idinfo
	except ValueError as e:
		print(e)
		return False

	return True


# Create your views here.

def reject_if_unauthorized(default, request, *args, **kwargs):
	if verify_google_token(request.headers.get('Authorization')):
		return default(request, *args, **kwargs)
	else:
		# Return 401 Unauthorized
		return Response(status=401)


class PodcastList(generics.ListAPIView):
	queryset = Podcast.objects.all()
	serializer_class = PodcastSerializer

	def list(self, request, *args, **kwargs):
		return reject_if_unauthorized(super().list, request, *args, **kwargs)


class PodcastSearch(generics.ListAPIView):
	serializer_class = PodcastSerializer

	def get_queryset(self):
		query = self.request.GET.get('title')
		return Podcast.objects.filter(title__icontains=query)

	def list(self, request, *args, **kwargs):
		return reject_if_unauthorized(super().list, request, *args, **kwargs)


class EpisodeList(generics.ListAPIView):
	serializer_class = EpisodeSerializer

	def get_queryset(self):
		podcast_id = self.kwargs['podcast_id']
		get_object_or_404(Podcast, id=podcast_id)
		return Episode.objects.filter(podcast_id=podcast_id)

	def list(self, request, *args, **kwargs):
		return reject_if_unauthorized(super().list, request, *args, **kwargs)


class IndividualEpisode(generics.RetrieveAPIView):
	serializer_class = EpisodeSerializer

	def get_object(self):
		return get_object_or_404(Episode, id=self.kwargs['episode_id'])

	def retrieve(self, request, *args, **kwargs):
		return reject_if_unauthorized(super().retrieve, request, *args, **kwargs)


class IndividualPodcast(generics.RetrieveAPIView):
	serializer_class = PodcastSerializer

	def get_object(self):
		return get_object_or_404(Podcast, id=self.kwargs['podcast_id'])

	def retrieve(self, request, *args, **kwargs):
		return reject_if_unauthorized(super().retrieve, request, *args, **kwargs)


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
