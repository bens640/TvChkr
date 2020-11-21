import json
from collections import defaultdict
from dateutil.parser import *

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites import requests
import requests
from TvChkr.settings import TMDB_API
from .models import StShow, Show
from users.models import Group, Membership

def genre_list():
    url = 'https://api.themoviedb.org/3/genre/tv/list?api_key=' + TMDB_API + '&language=en-US'
    response = requests.get(url)
    results = json.loads(response.text)
    data = results['genres']
    list = []
    for x in data:
        list.append(x)

    print(list)
    return list


def add_show(request, pk):
    url = 'https://api.themoviedb.org/3/tv/' + str(pk) + '?api_key=' + TMDB_API + '&language=en-US'
    response = requests.get(url)
    data = json.loads(response.text)
    if data['next_episode_to_air']:
        next_airdate = parse(data['next_episode_to_air']['air_date'])
    else:
        next_airdate = False

    if StShow.objects.filter(user=request.user) and StShow.objects.filter(show=data['id']):

        messages.success(request, data['name'] + ' is already in your watchlist')
    elif Show.objects.filter(show_num=data['id']).exists():
        s1 = Show.objects.get(show_num=data['id'])
        ss = StShow(show=s1, user=request.user)
        ss.save()
        messages.success(request, data['name'] + ' has been added')

    else:
        if next_airdate:
            s = Show(user=request.user, show_num = data['id'], title = data['name'], poster_path=data['poster_path'],
                     airdate=next_airdate)
            s.save()
        else:
            s = Show(user=request.user, show_num=data['id'], title=data['name'], poster_path=data['poster_path'])
            s.save()

        ss = StShow(show=s, user=request.user)
        ss.save()
        messages.success(request, data['name'] + ' has been added')
        print("Created and saved")

def remove_show(request, pk):
    current_show = Show.objects.filter(show_num=pk).first()
    show = StShow.objects.filter(show = current_show, user = request.user)
    show.delete()
    print(current_show.title +' has been deleted from '+ request.user.username + '\'s watchlist')
    messages.warning(request,'This show has been removed from your watchlist')


def add_show_to_group(request, pk, group):
    return True
def remove_show_user(request, show):
    x = StShow.objects.get(user=request.user, show = show)
    x.delete()


'''def update_show_date():
    for show in Show.objects.all():
        if show.airdate:
            show.airdate = get_new_airdate(show.show_num)
            show.save()


def get_new_airdate(pk):
    response = requests.get(
        'https://api.themoviedb.org/3/tv/' + str(pk) + '?api_key=' + TMDB_API + '&language=en-US')
    data = json.loads(response.text)
    if data['next_episode_to_air']:
        next_airdate = parse(data['next_episode_to_air']['air_date'])

        return next_airdate'''
