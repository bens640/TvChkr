import json
import requests

from django.contrib.sites import requests
from dateutil.parser import *
from TvChkr.settings import TMDB_API
from tv.models import Show


def update_show_date():
    for show in Show.objects.all():
        show.airdate = get_new_airdate(show.show_num)


def get_new_airdate(pk):
    response = requests.get(
        'https://api.themoviedb.org/3/tv/' + str(pk) + '?api_key=' + TMDB_API + '&language=en-US')
    data = json.loads(response.text)
    if data['next_episode_to_air']:
        next_airdate = parse(data['next_episode_to_air']['air_date'])
    else:
        next_airdate = False
    return next_airdate
