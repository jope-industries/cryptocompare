#!/usr/bin/env python

import cryptocompare
import datetime
import time
import unittest

coins = ['BTC', 'ETH', 'XMR', 'NEO']
currencies = ['EUR', 'USD', 'GBP']

class TestCryptoCompare(unittest.TestCase):

    def test_get_histo_day_no_params(self):
        res = cryptocompare.get_histo_day(coins[0])
        self.assertTrue('Data' in res.keys(), "expected 'Data'")
        # XXX: cryptocompare is off-by-one
        self.assertEqual(31, len(res['Data']), "response data defaults to 31 days")

    def test_get_histo_day_params(self):
        res = cryptocompare.get_histo_day(coins[0], params={'limit': 90})
        self.assertTrue('Data' in res.keys(), "expected 'Data'")
        # XXX: cryptocompare is off-by-one
        self.assertEqual(91, len(res['Data']), "expected limit to match days returned, got {}".format(len(res['Data'])))

    def test_get_coin_list(self):
        res = cryptocompare.get_coin_list()
        self.assertEqual(type(res), dict, "expected dict")
        self.assertTrue(len(res.keys()) > 0, "expected data")

    def test_get_coin_list_format(self):
        res = cryptocompare.get_coin_list(True)
        self.assertEqual(type(res), list, "expected list")
        self.assertTrue(len(res) > 0, "expected data")

    def test_get_price(self):
        print "-- testing get_price() --"
        cryptocompare.get_price(coins[0])
        cryptocompare.get_price(coins[1], curr='USD')
        cryptocompare.get_price(coins[2], curr=['EUR','USD','GBP'])
        cryptocompare.get_price(coins[2], curr=['EUR','USD','GBP'])
        cryptocompare.get_price(coins[2], full=True)
        cryptocompare.get_price(coins[0], curr='USD', full=True)
        cryptocompare.get_price(coins[1], curr=['EUR','USD','GBP'], full=True)
        cryptocompare.get_price(coins)
        cryptocompare.get_price(coins, curr='USD')
        cryptocompare.get_price(coins, curr=['EUR','USD','GBP'])

    def test_get_historical_price(self):
        print "-- testing get_historical_price() --"
        cryptocompare.get_historical_price(coins[0])
        cryptocompare.get_historical_price(coins[0], curr='USD')
        cryptocompare.get_historical_price(coins[1], curr=['EUR','USD','GBP'])
        cryptocompare.get_historical_price(coins[1], 'USD',datetime.datetime.now())
        cryptocompare.get_historical_price(coins[2], ['EUR','USD','GBP'],time.time())

    def test_get_historical_price_hour(self):
        print "-- testing get_historical_price_hour() --"
        cryptocompare.get_historical_price_hour(coins[0])
        cryptocompare.get_historical_price_hour(coins[0], curr='USD')
        cryptocompare.get_historical_price_hour(coins[1], curr=['EUR','USD','GBP'])

    def test_get_avg(self):
        print "-- testing get_avg() --"
        cryptocompare.get_avg(coins[0], markets='Coinbase')
        cryptocompare.get_avg(coins[0], curr='USD', markets='Coinbase')

if __name__ == '__main__':
    unittest.main()
