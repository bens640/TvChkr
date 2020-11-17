import json
from collections import defaultdict

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
    if Show.objects.filter(show_num=data['id']).exists():
        s1 = Show.objects.get(show_num=data['id'])
        ss = StShow(show=s1, user=request.user)
        ss.save()
        messages.success(request, data['name'] + ' has been added')

    else:
        s = Show(user=request.user, show_num = data['id'], title = data['name'], poster_path=data['poster_path'])
        s.save()

        ss = StShow(show=s, user=request.user)
        ss.save()
        messages.success(request, data['name'] + ' has been added')
        print("Created and saved")


def add_user_to_group(request, pk):
    if Group.objects.get(id=pk):
        if Membership.objects(person=request.user, group=pk):
            m1 = Membership(person = request.user, group=pk)
            m1.save()