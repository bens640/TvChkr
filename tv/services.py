import json
from collections import defaultdict

from django.contrib.auth.models import User
from django.contrib.sites import requests
import requests
from TvChkr.settings import TMDB_API
from .models import StShow,Show

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

def get_top():
    url = 'https://api.themoviedb.org/3/tv/popular?api_key='+TMDB_API+'&language=en-US&page=1'

    response = requests.get(url)
    results = json.loads(response.text)
    data = results['results']
    dict = {}
    for x in data:
        print(x)

        for k, v in x:
            print (k+v)
            dict[k] = v

    print(dict)


    return var


'''def add_show(request,pk):
    response = requests.get(
        'https://api.themoviedb.org/3/tv/' + pk + '?api_key=' + TMDB_API + '&language=en-US')
    data = json.loads(response.text)
    Show.objects.get_or_create(id = data['id'], title=['name'])
    if Show.objects.filter(id=data['id']).exists():
        s1 = Show.objects.filter(id=data['id'])
        ss = StShow(show=id, user=request.user)
        ss.save()
        print("Saved")
    else:
        s = Show(user=request.user)
        s.show_id=data['id']
        s.save()
        ss = StShow(show=s, user=request.user)
        ss.save()
        print("Created and saved")
'''