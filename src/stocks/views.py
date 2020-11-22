import requests
import logging
import datetime
from django.shortcuts import render
from django.conf import settings

# Stock class which holds all pertinent data relating to
# each selected stock

class Stock:
    def __init__(self, name, price, change):
        self.name = name
        self.change = str(round(change, 2)) + '%'
        if change >= 0:
            self.gain = True
        else:
            self.gain = False

        if (price * 100) % 10 == 0:
            self.price = '$' + str(round(price, 2)) + '0'
        else:
            self.price = '$' + str(round(price, 2))

logger = logging.getLogger('myweb.API')
logger.info('API called on: ' + str(datetime.datetime.now()))
# Store API info in settings.py then import into other views
#https://stackoverflow.com/questions/52030957/how-to-hide-google-map-api-key-in-django-before-pushing-it-on-github
def my_stocks(request):

    
    logger = logging.getLogger('myweb.requests')

    url = settings.YAHOO_API_URL

    querystring = {"symbols": settings.YAHOO_API_PICKS, "region": "US"}

    headers = {
        'x-rapidapi-host': settings.YAHOO_API_HOST,
        'x-rapidapi-key': settings.YAHOO_API_KEY
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()

  
    # collect necessary data
    # Ticker name, market hour price, and market hour change
    stock_data = {
        'ticker_first': response['quoteResponse']['result'][0]['symbol'],
        'price_first': response['quoteResponse']['result'][0]['regularMarketPrice'],
        'change_first': response['quoteResponse']['result'][0]['regularMarketChangePercent'],
        # second pick
        'ticker_second': response['quoteResponse']['result'][1]['symbol'],
        'price_second': response['quoteResponse']['result'][1]['regularMarketPrice'],
        'change_second': response['quoteResponse']['result'][1]['regularMarketChangePercent'],
        # third pick
        'ticker_third': response['quoteResponse']['result'][2]['symbol'],
        'price_third': response['quoteResponse']['result'][2]['regularMarketPrice'],
        'change_third': response['quoteResponse']['result'][2]['regularMarketChangePercent']
    }

    # create Stock object
    picks = {
        'top': Stock(stock_data['ticker_first'], stock_data['price_first'], stock_data['change_first']),
        'second': Stock(stock_data['ticker_second'], stock_data['price_second'], stock_data['change_second']),
        'third': Stock(stock_data['ticker_third'], stock_data['price_third'], stock_data['change_third'])
    }

    context = {'picks': picks,'FONTAWESOME_KEY': settings.FONTAWESOME_KEY}
    logger.error('API call FAILED on: ' + str(datetime.datetime.now()))
    return render(request, 'stocks.html', context)
