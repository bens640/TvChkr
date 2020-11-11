from django.shortcuts import render
from TvChkr.settings import API_KEY
from .models import Show
import requests
import json


URL = 'https://api.themoviedb.org/3/'


def home(request):
    context = {
        'shows': Show.objects.all
    }
    return render(request, 'tv/home.html', context)


def apitest(request):
    response = requests.get(
        'https://api.themoviedb.org/3/search/tv?api_key=' + API_KEY + '&language=en-US&page=1&query=mandalorian&include_adult=false')

    parsed_data = json.loads(response.text)
    data = []
    results = (parsed_data['results'])

    # print(parsed_data)
    for x in results:
        data.append(x)
    return render(request, 'tv/apitest.html', {"data": data})


def show_top(request):
    response = requests.get('https://api.themoviedb.org/3/tv/top_rated?api_key=' + API_KEY + '&language=en-US&page=1')
    parsed_data = json.loads(response.text)
    data = []
    results = (parsed_data['results'])
    for x in results:
        data.append(x)

    return render(request, 'tv/top_rated.html', {"data": data})


def playing_today(request):
    response = requests.get(
        'https://api.themoviedb.org/3/tv/airing_today?api_key=' + API_KEY + '&language=en-US&page=1')
    parsed_data = json.loads(response.text)
    data = []
    results = (parsed_data['results'])
    for x in results:
        data.append(x)

    return render(request, 'tv/today.html', {"data": data})


def detail(request):
    show_id = '82856';
    response = requests.get(
        'https://api.themoviedb.org/3/tv/82856?api_key=440a590b366bd1f9b7e362d4d3715fb1&language=en-US')
    parsed_data = json.loads(response.text)
    print(parsed_data)
    print('*******************')
    data = []
    for x in parsed_data:
        data.append(x)

    return render(request, 'tv/today.html', {"data": data})


def about(request):
    return render(request, 'tv/about.html', {'title': 'About'})
