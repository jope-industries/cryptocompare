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

    def test_get_histo_hour_no_params(self):
        res = cryptocompare.get_histo_hour('BTC')
        self.assertTrue('Data' in res.keys(), "expected 'Data'")
        # XXX: cryptocompare is off-by-one
        self.assertEqual(169, len(res['Data']), "response data defaults to 11 days")

    def test_get_histo_hour_params(self):
        res = cryptocompare.get_histo_hour('BTC', 'USD', params={'limit': 10})
        self.assertTrue('Data' in res.keys(), "expected 'Data'")
        # XXX: cryptocompare is off-by-one
        self.assertEqual(11, len(res['Data']), "response data defaults to 11 days")

    # def test_catchall(arg):
        # print('================== HIST PRICE DAY ================')
        # print(cryptocompare.get_historical_price_day(coins[0]))
        # print(cryptocompare.get_historical_price_day(coins[0], curr='USD'))
        # print(cryptocompare.get_historical_price_day(coins[1], curr=['EUR','USD','GBP']))
        #
        # print('======================== AVG =====================')
        # print(cryptocompare.get_avg(coins[0], markets='Coinbase'))
        # print(cryptocompare.get_avg(coins[0], curr='USD', markets='Coinbase'))
        #
        # print('====================== EXCHANGES =================')
        # print(cryptocompare.get_exchanges())

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
    TestCryptoCompare.test_catchall()
