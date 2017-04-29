from django.conf.urls import url
from . import views

app_name = 'backend'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # /teams/
    url(r'^teams/$', views.teams_overview, name='teams_overview'),

    # /players/
    url(r'^players/$', views.players_overview, name='players_overview'),

    # /games/
    url(r'^games/$', views.games_overview, name='games_overview'),

    # /team/<team_id>
    url(r'^team/(?P<team_id>[A-Z]+)/$', views.team_detail, name='team_detail'),

    # /player/<player_id>
    url(r'^player/(?P<player_id>[0-9]+)/$', views.player_detail, name='player_detail')
]