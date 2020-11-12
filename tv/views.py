from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from TvChkr.settings import TMDB_API
from .models import Show
from django.contrib.auth.models import User
import requests
import json
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import os


URL = 'https://api.themoviedb.org/3/'


def home(request):
    context = {
        'shows': Show.objects.all
    }
    return render(request, 'tv/home.html', context)


class ShowlistView(ListView):
    model = Show
    template_name = 'tv/home.html'
    context_object_name = 'shows'
    ordering = ['airdate']
    paginate_by = 4


class UserlistView(ListView):
    model = Show
    template_name = 'tv/user_show.html'
    context_object_name = 'shows'

    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Show.objects.filter(user=user).order_by('-airdate')

class ShowDetailView(DetailView):
    model = Show


class ShowCreateView(LoginRequiredMixin, CreateView):
    model = Show
    fields = ['title', 'genre', 'airdate']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ShowUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Show
    fields = ['title', 'genre', 'airdate']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        show = self.get_object()
        if self.request.user == show.user:
            return True
        return False


class ShowDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Show
    success_url = '/'

    def test_func(self):
        show = self.get_object()
        if self.request.user == show.user:
            return True
        return False



def apitest(request):
    response = requests.get(
        'https://api.themoviedb.org/3/tv/on_the_air?api_key=' + TMDB_API + '&language=en-US&page=1&query=mandalorian&include_adult=false')

    parsed_data = json.loads(response.text)
    data = []
    results = (parsed_data['results'])

    # print(parsed_data)
    for x in parsed_data:
        # data.append(x)
        data = Show(title=x['name'], airdate =x['first_air_date'], genre=x['genre_ids'], user_id = 1)
        data.save()
    return render(request, 'tv/apitest.html')


def show_top(request):
    response = requests.get('https://api.themoviedb.org/3/tv/top_rated?api_key=' + TMDB_API + '&language=en-US&page=1')
    parsed_data = json.loads(response.text)
    data = []
    results = (parsed_data['results'])
    for x in results:
        data.append(x)

    return render(request, 'tv/top_rated.html', {"data": data})


def playing_today(request):
    response = requests.get(
        'https://api.themoviedb.org/3/tv/airing_today?api_key=' + TMDB_API + '&language=en-US&page=1')
    parsed_data = json.loads(response.text)
    data = []
    results = (parsed_data['results'])
    for x in results:
        data.append(x)

    return render(request, 'tv/today.html', {"data": data})


def detail(request):
    show_id = '82856';
    response = requests.get(
        'https://api.themoviedb.org/3/tv/'+show_id+'?api_key='+TMDB_API+'&language=en-US')
    parsed_data = json.loads(response.text)
    print(parsed_data)
    print('*******************')
    data = []
    for x in parsed_data:
        data.append(x)

    return render(request, 'tv/today.html', {"data": data})


def about(request):
    return render(request, 'tv/about.html', {'title': 'About'})
