from django.conf.urls import url
from . import views

app_name = 'backend'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^teams/$', views.teams_overview, name='teams_overview'),
    url(r'^players/$', views.players_overview, name='players_overview'),
    url(r'^teams/(?P<team_id>[A-Z]+)/$', views.team_detail, name='teams_detail')
]