from django.conf.urls import url
from django.urls import path
from . import views
# from .services import add_show
from .views import ShowlistView, ShowCreateView, ShowUpdateView, \
    ShowDeleteView, UserlistView, SearchResultsView, DetailTemplateView, TopTemplateView

urlpatterns = [
    path('', ShowlistView.as_view(), name='tv-home'),
    path('user/<str:username>', UserlistView.as_view(), name='user-show'),
    path('about/', views.about, name='tv-about'),
    path('top/', TopTemplateView.as_view(), name='tv-top'),
    path('show/new/', ShowCreateView.as_view(), name='tv-create'),
    path('show/<int:pk>/update', ShowUpdateView.as_view(), name='tv-update'),
    path('show/<int:pk>/delete', ShowDeleteView.as_view(), name='tv-delete'),
    path('apitest/', views.apitest, name='tv-api'),
    # path('top/', views.about, name='tv-top'),
    path('today/', views.playing_today, name='tv-today'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('show/<int:pk>/', DetailTemplateView.as_view(), name='tv-detail'),

]

