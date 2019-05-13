import hmac,hashlib
import urllib,urllib2,json
import pprint,time
import sys, getopt
import numpy as np
from poloniex import poloniex
import datetime

##################
# User Interface #
##################
backtest = True
FIT = True
N = 1000

APIK= 'HGKS3KMW-R1DRG5CJ-MMTPHA40-JVN9DR7L'
APIS='2670d0a7345b1529bc5ea43e993708c6c0a1216370d898bca83b29f32ac7734bb1767791c16ee4311229a6fdfb6819373d513eb2fc4955730c713e8b70e32d4c'

API=poloniex(str(APIK),str(APIS))

exchange = 'poloniex'
Pair = 'USDT_BTC'
period = 14400

pnEMAfast = 17
pnEMAslow = 56
pnMAslow = 50
pnRSI = 14
pdelay = 14
psl = 0.30

params = [pnEMAfast,pnEMAslow,pnMAslow,pnRSI,pdelay,psl]
	
############
# Strategy #
############

def buyTrigger (prices, nEMAslow, nEMAfast, nMAslow, nRSI):

        trend = SMA(prices,nMAslow) - SMA(prices,nMAslow,1)
        BollingerD = MAslow - 2*bollinger(prices,MAslow,nslow)
        BollingerU = MAslow + 2*bollinger(prices,MAslow,nslow)
        EMAslow, EMAfast, macd = MACD(prices,nfast,nslow)
	rsi = RSI(prices,nRSI)
	
	return result

def sellTrigger (prices, nEMAslow, nEMAfast, nMAslow, nRSI,stopLoss):

        trend = SMA(prices,nMAslow) - SMA(prices,nMAslow,1)
        BollingerD = MAslow - 2*bollinger(prices,MAslow,nslow)
        BollingerU = MAslow + 2*bollinger(prices,MAslow,nslow)
        EMAslow, EMAfast, macd = MACD(prices,nfast,nslow)
        rsi = RSI(prices,nRSI)

	return result,stopLoss

##############
# Indicators #
##############

def bollinger (prices,MAslow,nslow):
	temp = 0
	for i in range(nslow):
		temp += (prices[-i-1]-MAslow)**2
	temp = (temp/nslow)**0.5
	return temp

def SMA (prices,length, delta = 0):
	if delta == 0:
		result = sum(prices[-length:])/float(length)
	else:
		result = sum(prices[-length-delta:-delta])/float(length)
	return result

def EMA (prices, length, delta = 0):
	if delta == 0:
		prices = prices[-length:]
	else:
		prices = prices[-length-delta:-delta]
	temp = prices[0]
	a = 2.0/(float(length+1))
	for i in range(1,len(prices)-delta):
		temp  = a*prices[i] + (1-a) * temp
	return temp

def RSI(prices,length, delta = 0):
	if delta == 0:
		x = np.asarray(prices[-lengthi-1:])
	else:
		x = np.asarray(prises[-length-1-delta:-delta])
	diff = np.diff(x)
	H = diff[np.diff >= 0 ].sum()/length
	L = diff[np.diff < 0 ].sum()/length
	RSI = H/(H+L)*100
	return RSI

def MACD(prices,nslow,nfast,delta =0):
	emaslow = EMA(prices,nslow,delta)
	emafast = EMA(prices,nfast,delta)
	return emaslow, emafast, emaslow - emafast
 
############
# Bot Core #
############

def trade(c1,b1,c2,b2,opens,closes,highs,lows,prices,position,stopLoss,dates,volumes,trades,params):
	nEMAfast = params[0]
	nEMAslow = params[1]
	nMAslow = params[2]
	nRSI = params[3]
	delay = params[4]
	sl = params[5]
	if len(opens)>nEMAslow:
		if len(trades) > 0:
			dt = dates[-1]-trades[-1][0]
		else:
			dt = 11
		MAslow = SMA(prices,nMAslow)
		MAslowold = SMA(prices,nMAslow,1)
		BollingerD = MAslow - 2*bollinger(prices,MAslow,nMAslow)
		BollingerU = MAslow + 2*bollinger(prices,MAslow,nMAslow)
		EMAslow, EMAfast, macd = MACD(prices,nEMAfast,nEMAslow)
		oldEMAslow,oldEMAfast, oldmacd = MACD(prices,nEMAfast,nEMAslow,1)
		if prices[-1]>prices[-2]:
			stopLoss = prices[-1]*(1-sl)
		if oldmacd < macd  and position == 'closed' and dt > delay:
			position = 'open'
			b2 = b1 / closes[-1] * (1-0.0015)
			b1 = 0
			stopLoss = closes[-1] * (1-sl)
			trades.append([dates[-1],closes[-1],'buy'])
		elif ((macd < oldmacd  and dt > delay) or closes[-1] < stopLoss) and position == 'open' :
			position = 'closed'
			b1 = b2 * closes[-1] * (1-0.0015)
			b2 = 0
			stopLoss = 0
			trades.append([dates[-1],closes[-1],'close'])
		if b1+b2 == 0:
			sys.exit()
	return(c1,b1,c2,b2,opens,closes,highs,lows,prices,position,stopLoss,dates,volumes,trades)

##################
# Initialisation #
##################

position = 'closed'
c1 = Pair.split('_')[0]
c2 = Pair.split('_')[1]

if backtest:
	b1  = 100.0
	b2 = 0.0

else:
	balance = API.returnBalances()
	b1 = balance[c1]
	b2 = balance[c2]

#print('balance {} = {}, balance {} = {}'.format(c1,b1,c2,b2))
startTime = int(time.time())-int(time.time())%int(period)
stopLoss = 0

chartData = []
dates = []
volumes = []
opens = []
closes = []
highs = []
lows = []
prices = []
trades = []

if backtest:
	
	if FIT:
		with open('sample.json', 'r') as fp:
			temp = json.load(fp)
	else:

		endTime = int(time.time())-int(time.time())%int(period)
		startTime = int(time.time())-int(time.time())%int(period)-N*int(period)

		temp = API.api_query("returnChartData",{"currencyPair":Pair,"start":startTime,"end":endTime,"period":period})

       	for i in range(len(temp)):
		dates.append(float(temp[i]['date'])/float(period)-startTime/int(period))
		volumes.append(float(temp[i]['volume']))
	       	opens.append(float(temp[i]['open']))
       		closes.append(float(temp[i]['close']))
	       	highs.append(float(temp[i]['high']))
       		lows.append(float(temp[i]['low']))
       		prices.append((temp[i]['low']+temp[i]['high']+temp[i]['close'])/3.0)
		c1,b1,c2,b2,opens,closes,highs,lows,prices,position,stopLoss,dates,volumes,tardes = trade(c1,b1,c2,b2,opens,closes,highs,lows,prices,position,stopLoss,dates,volumes,trades,params)
	print('{}\t{}\t{}\t{}\t{}'.format(pnEMAfast,pnEMAslow,pdelay,psl,b1+(b2*closes[-1])))

else:
	while True:
	
		endTime = int(time.time())-int(time.time())%int(period)-int(period)

		probe = False

		if endTime > startTime:
			try:
				temp = API.api_query("returnChartData",{"currencyPair":Pair,"start":startTime,"end":endTime,"period":period})
				temp = temp [-1]
				probe = True
        		except urllib2.URLError:
                		time.sleep(int(30))

        	if probe:
			opens.append(temp['open'])
			closes.append(temp['close'])
			highs.append(temp['high'])
			lows.append(temp['low'])
			prices.append((temp['low']+temp['high']+temp['close'])/3.0)
			print('price = {}, high = {}, low = {}, close = {}'.format(prices[-1],highs[-1],lows[-1],closes[-1]))
		if len(opens)>20:
			MA20 = sum(prices[-20:-1])/20.0
			MA20old = sum(prices[-21:-2])/20.0
			if closes[-1] > MA20 and MA20 > MA20old and position == 'closed':
				position = 'open'
				b2 = b1 / closes[-1] * (1-0.0025)
				b1 = 0
				stopLoss = closes[-1] * (1-0.03)
				print('Position Opened at price = {}, {} balance = {}'.format(closes[-1],c1,b2*closes[-1]))
			if (closes[-1] < MA20 or close[-1] < stopLoss) and position == 'open':
				position = 'closed'
				b1 = b2 * closes[-1] * (1-0.0025)
				b2 = 0
				print('Position Closed at price = {}, {} balance = {}'.format(closes[-1],c1,b1))

		startTime = endTime	
        	time.sleep(int(30))

#########
