from datetime import date
from dateutil.parser import *
from dateutil.utils import today
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from TvChkr.settings import TMDB_API, PLACEHOLDER_IMAGE
from users.models import Group, Membership
from .models import Show, StShow
from django.contrib.auth.models import User
import requests
import json
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from django.contrib import messages
from .forms import GroupUpdateForm
from .services import add_show, add_show_to_group, remove_show
import feedparser


class SearchResultsView(ListView):
    model = Show
    template_name = 'tv/show_results.html'
    context_object_name = 'shows'

    def get_queryset(self):

        if self.request.GET.get('q'):
            formatted_query = self.request.GET.get('q')

        else:
            formatted_query = 'the'

        response = requests.get(
            'https://api.themoviedb.org/3/search/tv?api_key=' + TMDB_API + '&language=en-US&query=' + formatted_query + '&include_adult=false')
        parsed_data = json.loads(response.text)
        data = []
        results = (parsed_data['results'])
        for x in results:
            data.append(x)
        # object_list = Show.objects.filter(Q(title__icontains=query) | Q(genre__icontains=query))

        return data


class ShowlistView(ListView):
    # update_show_date()
    model = Show
    template_name = 'tv/home.html'
    context_object_name = 'shows'
    ordering = ['-airdate']
    paginate_by = 9

    # genres = services.genre_list()


class UserlistView(ListView):
    model = Show
    template_name = 'tv/user_show.html'
    context_object_name = 'shows'

    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))

        return Show.objects.filter(user=user).order_by('-airdate')


class ShowCreateView(LoginRequiredMixin, CreateView):
    model = Show
    # template_name = 'tv/show_form.html'
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


class ShowDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Show
    success_url = '/'

    def test_func(self):
        show = self.get_object()
        if self.request.user == show.user:
            return True
        return False


def show_detail(request, pk):
    response = requests.get(
        'https://api.themoviedb.org/3/tv/' + str(pk) + '?api_key=' + TMDB_API + '&language=en-US')
    data = json.loads(response.text)
    current_show = Show.objects.filter(show_num=data['id']).first()
    my_groups = Membership.objects.filter(person=request.user)
    user_info = StShow.objects.filter(show=current_show).filter(user=request.user).first()
    if data['next_episode_to_air']:
        next_air = parse(data['next_episode_to_air']['air_date']).date()
    else:
        next_air = 'TBD'
    if request.POST.get('add_show', ""):
        add_show(request, pk)
        return redirect(show_detail, data['id'])
    elif request.POST.get('remove_show', ""):
        remove_show(request, pk)
        print('remove')
        return redirect(show_detail, data['id'])

    return render(request, 'tv/show_detail.html', {"show": data, 'groups': my_groups,
                                                   'user_info': user_info,
                                                   'airdate': next_air})


def apitest(request):
    response = requests.get(
        'https://api.themoviedb.org/3/tv/on_the_air?api_key=' + TMDB_API + '&language=en-US&page=1&query=mandalorian&include_adult=false')
    parsed_data = json.loads(response.text)
    data = []
    results = (parsed_data['results'])
    return render(request, 'tv/apitest.html', {"show": results})


def playing_today(request):
    response = requests.get(
        'https://api.themoviedb.org/3/tv/airing_today?api_key=' + TMDB_API + '&language=en-US&page=1')
    parsed_data = json.loads(response.text)
    data = []
    results = (parsed_data['results'])
    for x in results:
        data.append(x)
    return render(request, 'tv/today.html', {"data": data})


def feed(request):
    d = feedparser.parse('https://rss.tvguide.com/breakingnews/')
    return render(request, 'tv/feed.html', {'feeds': d})


class ModelTestView(ListView):
    model = StShow
    template_name = 'tv/home.html'
    context_object_name = "shows"


class TopTemplateView(TemplateView):
    context_object_name = 'show'
    template_name = 'tv/top_rated.html'

    def get_context_data(self, **kwargs):
        url = 'https://api.themoviedb.org/3/tv/popular?api_key=' + TMDB_API + '&language=en-US&page=1'
        response = requests.get(url)
        parsed_data = json.loads(response.text)
        return parsed_data


class DetailTemplateView(TemplateView):
    context_object_name = 'show'
    template_name = 'tv/show_detail.html'

    def get_context_data(self, **kwargs):
        query = str(self.kwargs.get('pk'))
        url = 'https://api.themoviedb.org/3/tv/' + query + '?api_key=' + TMDB_API + '&language=en-US'
        response = requests.get(url)
        context = json.loads(response.text)
        return context


class GroupCreateView(CreateView):
    model = Group
    template_name = 'tv/group_form.html'
    fields = ['name', 'about']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class GroupListView(ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'tv/groups.html'


class GroupDetailView(DetailView):
    model = Group
    template_name = 'tv/group_detail.html'

    def post(self, request, *args, **kwargs):
        print(self.kwargs.get('pk'))

        if Group.objects.get(id=self.kwargs.get('pk')):
            m1 = Membership(person=request.user, group=Group.objects.get(id=self.kwargs.get('pk')), date_joined=today())
            m1.save()
        return redirect('groups')

    def get_context_data(self, **kwargs):
        group = Group.objects.get(pk=self.kwargs.get('pk'))
        shows = StShow.objects.filter(group=group)
        context = {'group': group,
                   'users': group.members.all(),
                   'shows': shows}
        return context
