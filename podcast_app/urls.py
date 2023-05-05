from django.urls import path
from . import views

urlpatterns = [
    path('podcasts/', views.PodcastList.as_view(), name='podcast-list'),
    path('podcasts/<int:podcast_id>/', views.IndividualPodcast.as_view(), name='podcast'),
    path('podcasts/<int:podcast_id>/episodes/', views.EpisodeList.as_view(), name='episode-list'),
    path('podcasts/<int:podcast_id>/subscribe/', views.SubscribeToPodcast.as_view(), name='subscribe-podcast'),
    path('podcasts/<int:podcast_id>/unsubscribe/', views.UnsubscribeFromPodcast.as_view(), name='unsubscribe-podcast'),
    path('episodes/<int:episode_id>/', views.IndividualEpisode.as_view(), name='episode'),
    path('user/subscriptions/', views.UserSubscriptions.as_view(), name='user-subscriptions'),
]
