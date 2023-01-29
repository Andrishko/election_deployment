from django.urls import path

from . import views

urlpatterns = [
    path('api/gettokens', views.gettokens),
    path('api/getvotings', views.get_votings),
    path('test/<str:user_token>', views.test),
    path('votetest/', views.votetest),
    path('votesolo/', views.votesolo)
]

