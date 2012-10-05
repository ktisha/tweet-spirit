# coding=utf-8
__author__ = 'ktisha'

TWITTER_PAGE = "http://twitter.com/"

from twython import Twython

t = Twython()
query_string = 'параллелепипед'
t_search = t.search(q=query_string)

texts = []

def add_found_texts(t_search):
  for key in t_search['results']:
    texts.append(key['text'])
  if t_search.has_key('next_page'):
    print t_search['next_page']

add_found_texts(t_search)

i = 2
while t_search.has_key('next_page'):
  t_search = t.search(q = query_string, page = i)
  i += 1
  add_found_texts(t_search)

for text in texts:
  print(text)
  print()

#TODO: cut urls and RT from text, then analyze