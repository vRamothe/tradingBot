from poloniex import poloniex
import sys
import urllib, json
import pprint
from botcandlestick import BotCandlestick

class BotChart(object):
	def __init__(self, exchange, pair, period, backtest=True):
		self.pair = pair
		self.period = period

		self.startTime = 1491048000
		self.endTime = 1491591200

#		self.startTime = 9999999999-(period*10000)
#		self.endTime = 9999999999
		
		self.data = []
		
		if (exchange == "poloniex"):
			self.conn = poloniex('9IM81U4I-NRO2G2KZ-WJ3RQMTN-Q53YIYDH','fb092f17b981db2428dda4b4d8b593934efccde5208a6678a6d2ff3f435682568788cf38997950e0def5f69c65d70c3f17cc3092c89b99184654f859feb4f7d5')
			if backtest:
				poloData = self.conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
				self.conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
				sys.exit()
				for datum in poloData:
					if (datum['open'] and datum['close'] and datum['high'] and datum['low']):
						self.data.append(BotCandlestick(self.period,datum['open'],datum['close'],datum['high'],datum['low'],datum['weightedAverage']))
		if (exchange == "bittrex"):
			if backtest:
				url = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName="+self.pair+"&tickInterval="+self.period+"&_="+str(self.startTime)
				response = urllib.urlopen(url)
				rawdata = json.loads(response.read())

				self.data = rawdata["result"]
	def getPoints(self):
		return self.data

	def getCurrentPrice(self):
		currentValues = self.conn.api_query("returnTicker")
		lastPairPrice = {}
		lastPairPrice = currentValues[self.pair]["last"]
		return lastPairPrice
