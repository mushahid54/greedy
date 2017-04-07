from django.shortcuts import render

# Create your views here.

# class RetrieveResourceDetails(generics.RetrieveAPIView):
from django.conf import settings
import requests
from rest_framework import views, permissions, response, status


class ResourceSearchAPIView(views.APIView):
    """
    Get Multiple Resource response in One Request
    """
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, *args, **kwargs):
        query_term = request.query_params.get('q', None)
        # search for query term in parallel, on multiple sources
        google_results = self.__search_on_google(query_term)
        duckduckgo_results = self.__search_on_duck_duck_go(query_term)
        twitter_results = self.__search_on_twitter(query_term)

        # combine results
        response_data = {
            'query': query_term,
            'results': {
                'google': google_results,
                'duckduckgo': duckduckgo_results,
                'twitter': twitter_results

            }
        }

        # return result
        return response.Response(response_data, status=status.HTTP_200_OK)

    def __search_on_google(self, query_term):
        google_results = dict()
        params_dict = {
            'q': 'butterfly',  # query_term
            'key': settings.GOOGLE_API_KEY,
            'cx': settings.GOOGLE_API_CLIENT
        }
        url = 'https://www.googleapis.com/customsearch/v1'
        response = requests.get(url, params=params_dict)
        google_results['url'] = response.url
        google_results['text'] = response.json()['items'][0]['snippet']

        return google_results

    def __search_on_duck_duck_go(self, query_term):
        duckduckgo_results = dict()
        params_dict = {'q': 'butterfly', 'format': 'json'}
        url = 'http://api.duckduckgo.com/'
        response = requests.get(url, params=params_dict)
        duckduckgo_results['url'] = response.url
        duckduckgo_results['text'] = response.json()['RelatedTopics'][0]['Text']

        return duckduckgo_results

    def __search_on_twitter(self, query_term):
        twitter_results = dict()
        # twitter_token = "Bearer AAAAAAAAAAAAAAAAAAAAAB8U0AAAAAAAyL%2B2RFxVigwAMMlWhLhQW%2BqACOA%3DsVk4Z1zD0GxYDIGtndWd0g2kd02kRRIkDgmberfx4TYNJbhJHX",
        params_dict = {'q': 'butterfly'}
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        headers = {"Authorization": settings.TWITTER_ACCESS_TOKEN, "Content-Type": "application/json"}
        response = requests.get(url, params=params_dict, headers=headers)

        twitter_results['url'] = response.url
        try:
            twitter_results['text'] = response.json()['statuses'][0]['text']
        except IndexError:
            twitter_results['text'] = "No Tweet"

        return twitter_results

