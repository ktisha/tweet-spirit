__author__ = 'ktisha'

from django.core.cache import cache
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.tokenize import WordPunctTokenizer
from nltk.probability import FreqDist

FreqDist._N = 0 #For pickle of classifier
TWITTER_PAGE = "http://twitter.com/"
APP_KEY = 'iiDb1XiAgOX5LKVSUiK9Q'
APP_SECRET = 'z14Je2eFr9aMVNMwJPzwoPZluagT51UVntTHNjh0UZc'
OAUTH_TOKEN = '373568173-vYXDGggR4WfIXP28I3PTPKAKLVUIBtJqmygRgDJD'
OAUTH_TOKEN_SECRET = 'ILN8hHOgj4FDbfETPHAqgmkzW2DsZcPUqSofSyHgZ4'

def search_tweets(query_string):
    from twython import Twython

    t = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    t_search = t.search(q=query_string, lang='en')

    texts = []

    def add_found_texts(t_search):
        for key in t_search['statuses']:
            texts.append(key['text'])
        if t_search.has_key('next_page'):
            print t_search['next_page']

    add_found_texts(t_search)

    i = 2
    while t_search.has_key('next_page'):
        t_search = t.search(q = query_string, page = i)
        i += 1
        add_found_texts(t_search)

    return texts

def word_feats(words):
    return dict([(word, True) for word in words])

class AnalyzedTweet(object):
    text = ''
    pos = 0
    neg = 0

    def __init__(self, text, pos, neg):
        self.text = text
        self.pos = pos
        self.neg = neg

def analyze(tweets):
    classifier = cache.get('classifier')
    if classifier is None:
        classifier = train_classifier()
        cache.set('classifier', classifier, None)
    tokenizer = WordPunctTokenizer()
    analyzed_tweets = []
    for tweet in tweets:
        tokens = tokenizer.tokenize(tweet.lower())
        featureset = word_feats(tokens)
        sentiment = classifier.prob_classify(featureset)
        analyzed_tweets.append(AnalyzedTweet(tweet, round(sentiment.prob('pos'),2), round(sentiment.prob('neg'),2)))
    return analyzed_tweets

def train_classifier():
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')

    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

    trainfeats = negfeats + posfeats
    classifier = NaiveBayesClassifier.train(trainfeats)

    return classifier