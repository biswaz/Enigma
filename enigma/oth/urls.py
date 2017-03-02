from django.conf.urls import url

from . import views

urlpatterns = [


url(r'^finish/', views.FinishView.as_view(), name='finish'),
url(r'^play/', views.PlayView.as_view(), name='play_view'),
url(r'^leaderboard/', views.LeaderBoardView.as_view(), name='leaderboard_view'),


]
