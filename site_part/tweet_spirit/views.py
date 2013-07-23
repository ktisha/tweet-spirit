# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from utils import search_tweets, analyze

def search(request):
    return render_to_response("search.html", context_instance=RequestContext(request, {'initial_value': "Mickey"}))

def search_response(request):
    query_string = request.GET['searchField']
    tweets = search_tweets(query_string)
    analyzed_tweets = analyze(tweets)
    return render_to_response("response.html", context_instance=RequestContext(request, {'tweets': analyzed_tweets}))

