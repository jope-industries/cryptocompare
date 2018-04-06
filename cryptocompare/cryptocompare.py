import sys
import requests
import time
import datetime
try:
    #python2
    from urllib import urlencode
except ImportError:
    #python3
    from urllib.parse import urlencode

# API
URL_COIN_LIST = 'https://www.cryptocompare.com/api/data/coinlist/'
URL_PRICE = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms={}'
URL_PRICE_MULTI = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms={}'
URL_PRICE_MULTI_FULL = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}'
URL_HIST_PRICE = 'https://min-api.cryptocompare.com/data/pricehistorical?fsym={}&tsyms={}&ts={}'
URL_HIST_PRICE_DAY = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}'
URL_HIST_PRICE_HOUR = 'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym={}'
URL_AVG = 'https://min-api.cryptocompare.com/data/generateAvg?fsym={}&tsym={}&e={}'
URL_EXCHANGES = 'https://www.cryptocompare.com/api/data/exchanges'

# FIELDS
PRICE = 'PRICE'
HIGH = 'HIGH24HOUR'
LOW = 'LOW24HOUR'
VOLUME = 'VOLUME24HOUR'
CHANGE = 'CHANGE24HOUR'
CHANGE_PERCENT = 'CHANGEPCT24HOUR'
MARKETCAP = 'MKTCAP'

# DEFAULTS
CURR = 'EUR'

###############################################################################

def query_cryptocompare(url,errorCheck=True):
    try:
        response = requests.get(url).json()
    except Exception as e:
        print('Error getting coin information. %s' % str(e))
        return None
    # TODO: check for 'Response' and a value different than 'Success'
    if errorCheck and 'Response' in response.keys() and response['Response'] != 'Success':
        print response
        print('[ERROR] %s' % response['Message'])
        return None
    return response

def format_parameter(parameter):
    if isinstance(parameter, list):
        return ','.join(parameter)
    else:
        return parameter

def parameter_filter(p, allowed):
    common_keys = allowed.intersection(set(p.keys()))
    return dict((k, p[k]) for k in (common_keys))

###############################################################################

def get_coin_list(format=False):
    response = query_cryptocompare(URL_COIN_LIST, False)['Data']
    if format:
        return list(response.keys())
    else:
        return response

# TODO: add option to filter json response according to a list of fields
def get_price(coin, curr=CURR, full=False):
    if full:
        return query_cryptocompare(URL_PRICE_MULTI_FULL.format(format_parameter(coin),
            format_parameter(curr)))
    if isinstance(coin, list):
        return query_cryptocompare(URL_PRICE_MULTI.format(format_parameter(coin),
            format_parameter(curr)))
    else:
        return query_cryptocompare(URL_PRICE.format(coin, format_parameter(curr)))

def get_historical_price(coin, curr=CURR, timestamp=time.time()):
    if isinstance(timestamp, datetime.datetime):
        timestamp = time.mktime(timestamp.timetuple())
    return query_cryptocompare(URL_HIST_PRICE.format(coin, format_parameter(curr), int(timestamp)))

def get_historical_price_day(coin, curr=CURR):
    return query_cryptocompare(URL_HIST_PRICE_DAY.format(coin, format_parameter(curr)))

def get_historical_price_hour(coin, curr=CURR):
    return query_cryptocompare(URL_HIST_PRICE_HOUR.format(coin, format_parameter(curr)))

# === get_histo_day ===
def get_histo_day(coin, curr=CURR, params={}):
    """
    Allowed parameters include:
        fsym	string	true	 	From Symbol
        tsym	string	true	 	To Symbols
        e	string	true	CCCAGG	Name of exchange
        extraParams	string	false	NotAvailable	Name of your application
        sign	bool	false	false	If set to true, the server will sign the requests.
        tryConversion	bool	false	true	If set to false, it will try to get values without using any conversion at all
        aggregate	int	false	1	Max 30
        limit	int	false	30	Max 2000
        toTs	timestamp	false
        allData	bool	false	false	get all data

        From https://www.cryptocompare.com/api/#-api-data-histoday-

        Note: cryptocompare api has an error, where the limit is off-by-one.  For example, if you want 30 days, pass limit=29.
    """
    default_params = {
        'tsym': curr,
        'fsym': coin,
    }
    allowed_params = set(['fsym', 'tsym', 'e', 'extraParams', 'sign', 'tryConversion', 'aggregate', 'limit', 'toTs', 'allData'])
    filtered_params = parameter_filter(params, allowed_params)
    param_copy = default_params.copy()
    param_copy.update(filtered_params)
    res = query_cryptocompare(URL_HISTO_DAY.format(urlencode(param_copy)))
    return res

def get_avg(coin, curr=CURR, markets='CCCAGG'):
    response = query_cryptocompare(URL_AVG.format(coin, curr, format_parameter(markets)))
    if response:
        return response['RAW']

def get_exchanges():
    response = query_cryptocompare(URL_EXCHANGES)
    if response:
        return response['Data']
