from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

# class RetrieveResourceDetails(generics.RetrieveAPIView):
from django.conf import settings
import requests
from rest_framework import status
import multiprocessing as mp
from rest_framework.response import Response
from rest_framework.decorators import api_view


def get_search_data_stored_in_queue(queue):
    combined_result = {}
    result_1 = queue.get()
    result_2 = queue.get()
    result_3 = queue.get()
    combined_result.update(result_1)
    combined_result.update(result_2)
    combined_result.update(result_3)
    return combined_result

@api_view(('GET',))
def search_in_parallel(request):
    query_term = request.GET.get('q', None)
    if not query_term:
        response_data = {'status': 0, 'message': 'Empty query'}

    queue = mp.Queue()

    p1 = mp.Process(target=search_on_google, args=(queue, query_term))
    p2 = mp.Process(target=search_on_duck_duck_go, args=(queue, query_term))
    p3 = mp.Process(target=search_on_twitter, args=(queue, query_term))
    # start process
    p1.start()
    p2.start()
    p3.start()
    # Join Process
    p1.join()
    p2.join()
    p3.join()

    response_data = get_search_data_stored_in_queue(queue)

    final_response_data = {
        'query': query_term,
        'results': response_data
    }
    return Response(final_response_data, status=status.HTTP_200_OK)


def search_on_google(queue, query_term):
    google_results = dict()
    params_dict = {
        'q': query_term,
        'key': settings.GOOGLE_API_KEY,
        'cx': settings.GOOGLE_API_CLIENT
    }
    url = 'https://www.googleapis.com/customsearch/v1'
    response = requests.get(url, params=params_dict)
    google_results['url'] = response.url
    try:
        google_results['text'] = response.json()['items'][0]['snippet']
    except IndexError:
        google_results = "No Query"

    queue.put({'google': google_results})


def search_on_duck_duck_go(queue, query_term):
    duckduckgo_results = dict()
    params_dict = {'q': query_term, 'format': 'json'}
    url = 'http://api.duckduckgo.com/'
    response = requests.get(url, params=params_dict)
    duckduckgo_results['url'] = response.url
    try:
        duckduckgo_results['text'] = response.json()['RelatedTopics'][0]['Text']
    except IndexError:
        duckduckgo_results['text'] = "No Query"

    queue.put({'duckduckgo': duckduckgo_results})


def search_on_twitter(queue, query_term):
    twitter_results = dict()
    params_dict = {'q': query_term}
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    headers = {"Authorization": settings.TWITTER_ACCESS_TOKEN, "Content-Type": "application/json"}
    response = requests.get(url, params=params_dict, headers=headers)

    twitter_results['url'] = response.url
    try:
        twitter_results['text'] = response.json()['statuses'][0]['text']
    except IndexError:
        twitter_results['text'] = "No Tweet"

    queue.put({'twitter': twitter_results})


