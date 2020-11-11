from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='tv-home'),
    path('about/', views.about, name='tv-about'),
    path('apitest/', views.apitest, name='tv-api'),
    path('top/', views.show_top, name='tv-top'),
    path('today/', views.playing_today, name='tv-today'),
    path('show/', views.detail, name='tv-detail'),
]

