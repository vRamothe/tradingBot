import hmac,hashlib
import urllib,json
import pprint,time
import sys, getopt
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import datetime
import _tkinter
#import tkinter

import indicators
import strategies
import bot

#from matplotlib.finance import candlestick2_ohlc
#from mpl_finance import candlestick_ohlc
#import matplotlib.pyplot as plt

##################
# User Interface #
##################

inp = {}
i=0
with open('input.dat','r') as inpt:
    for line in inpt:
        line = line.split()
        i+=1
        if 1 < len(line) and len(line) >= 3:
            try :
                inp[line[0]]=int(line[-1])
            except:
                try:
                    inp[line[0]]=float(line[-1])
                except:
                    try:
                        if len(line) == 3:
                            if line[-1]=='True':
                                line[-1] = True
                            elif line[-1] == 'False':
                                line[-1] = False
                            inp[line[0]]=line[-1]
                        else:
                            inp[line[0]]=float(line[-1])
                    except:
                        print('something odd at line {}'.format(i))
                        print('input.dat can\'t be read properly')
                        print('program exit')
                        sys.exit()
        if len(line) > 1 and line[0] == 'SignalWeigths':
            try:
                line[2:] = map(float,line[2:])
                inp[line[0]] = np.asarray(line[2:])
            except:
                print('something odd at line {}'.format(i))
                print('input.dat can\'t be read properly')
                print('program exit')
                sys.exit()


if inp['exchange'] == 'poloniex':
    from APIs.poloniex import poloniex
    API=poloniex(inp['APIK'],inp['APIS'])
    c1 = inp['Pair'].split('_')[0]
    c2 = inp['Pair'].split('_')[1]
    def query(inp,startTime,endTime):
        result = API.api_query("returnChartData",{"currencyPair":inp['Pair'],"start":startTime,"end":endTime,"period":inp['period']})
        return result

elif inp['exchange'] == 'binance':
    import APIs.binance
    API= binance.set(inp['APIK'],inp['APIS'])
    if 'USDT' in inp['Pair']:
        c1 = 'UDST'
        c2 = inp['Pair'].replace(c1,'')
    elif 'BTC' in inp['Pair']:
        c1 = 'BTC'
        c2 = inp['Pair'].replace(c1,'')
    elif 'ETH' in inp['Pair']:
        c1 = 'ETH'
        c2 = inp['Pair'].replace(c1,'')
    elif 'BNB' in inp['Pair']:
        c1 = 'BNB'
        c2 = inp['Pair'].replace(c1,'')
    def query(inp,start,end):
        interval = 0
        intervals = [1,3,5,15,30,60,120,240,360,720,1440]
        intervalb = ['1m','3m','5m','15m','30m','1h','2h','4h','6h','12h','1d']
        for i in range(len(intervals)):
            if intervals[i] == (inp['period']/60):
                interval = intervalb[i]
        if interval == 0:
            print('period is not valid in input file')
            sys.exit()
        result = binance.klines(inp['Pair'], interval)#, startTime = start ,endTime = end)
        return result

else:
    print('error : no valid echange has be selected')
    print('you can use this bot on binance or poloniex. Please select one of theese')
    sys.exit()


##################
# Initialisation #
##################

position = 'closed'

if inp['backtest']:
    initialBalance = 100.
    b1  = initialBalance
    b2 = 0.0

else:
    balance = API.returnBalances()
    b1 = balance[c1]
    b2 = balance[c2]

print('balance {} = {}, balance {} = {}'.format(c1,b1,c2,b2))
startTime = int(time.time())-int(time.time())%inp['period']
stoploss = 0

Time = []
balance = [initialBalance]
B1 = []
B2 = []
Trend = []
SMA20Trend = []
EMA20Trend = []
chartData = []
dates = [0]
volumes = []
opens = []
closes = []
highs = []
lows = []
prices = []
trades = []
signals = []
devsignals = []
trend = [0]
psar = [0]

if inp['backtest']:

    if inp['FIT']:
        with open('sample.json', 'r') as fp:
            data = json.load(fp)
        data = pd.DataFrame.from_dict(data)
    else:

        endTime = int(time.time())-int(time.time())%inp['period']
        startTime = int(time.time())-int(time.time())%inp['period']-inp['N']*inp['period']

        data = query(inp,startTime,endTime)

        fid = open('sample.json','w')
        fid.write(json.dumps(data, indent = 4))
        fid.close()

        data = json_normalize(data)
        if inp['exchange']=='poloniex':
            data.date = data.date.astype(int).fillna(0.0)
        if inp['exchange']=='binance':
            date = pd.Series(data.openTime, name='data')
            data.join(date)


    data.volume = data.volume.astype(float).fillna(0.0)
    data.open = data.open.astype(float).fillna(0.0)
    data.low = data.low.astype(float).fillna(0.0)
    data.high = data.high.astype(float).fillna(0.0)
    data.close = data.close.astype(float).fillna(0.0)

    data = indicators.SMA(data,20)
    data = indicators.SMA(data,50)
    data = indicators.SMA(data,100)
    data = indicators.SMA(data,200)

    data = indicators.RSI(data,14)
    data = indicators.STOS(data,14,3,3)
    data = indicators.STORSIS(data,14,3,3)
    data = indicators.MACD(data,12,26)
    data = indicators.MOMENTUM(data,10)
    data = indicators.ATRE(data,14)
    data = indicators.BB(data,20,1.5)
    data = indicators.BB(data,50,2)
    data = indicators.ROC(data,9)
    data = indicators.TRIX(data,18)
    data = indicators.TRIX(data,9)
    data = indicators.MONEYFLOW(data,14)
    data = indicators.KC(data,20,1.5)
    data = indicators.PSAR(data)
    data = indicators.CHAIKINocs(data)
#        data = indicators.CHAIKINmf(data)
#        data = indicators.ADL(data,9)
#        data = indicators.OBV(data,1)
#        data.fillna(0)

    Signal, devSignal, norm = strategies.Signalsprocess(data,20)


    for i in range(1,len(data.high)):
        ii = i+1
        dates.append(i)
        opens.append(data.open[i])
        highs.append(data.high[i])
        lows.append(data.low[i])
        closes.append(data.close[i])
        signals.append(Signal[i])
        devsignals.append(devSignal[i])

        if i==0:
            Signals = 0
            B1.append(b1)
            B2.append(0)
            balance.append(B1[-1]+B2[-1])
            continue
        psar.append(data.PSAR[i])
        trend.append(data.PSARtrend[i])
        b1,b2,position,stoploss,trades = bot.update(b1,b2, opens, highs, lows, closes,\
                                                    position,stoploss,dates,trades,inp,Signal[i],\
                                                    devSignal[i], psar, trend)
        B1.append(b1)
        B2.append(b2*closes[-1])
        balance.append(B1[i-1]+B2[i-1])
    totale = b1+(b2*closes[-1])
    profit = (totale - initialBalance)/initialBalance*100


totalWin = 0
maxWin = 0
nWin = 0
totalLoss = 0
maxLoss = 0
nLoss = 0
ntrade = 0
p = 0
lWins = []
lLoss = []

for i in range(len(trades)-1):
    if trades[i][-1] != 'buy':
        continue
    buy = trades[i]
    sell = trades[i+1]
    spread = (sell[2]-buy[2])/(buy[2])*100
    if spread>0:
        totalWin += spread
        maxWin = max(maxWin,spread)
        nWin +=1
        lWins.append(spread)
    if spread<0:
        totalLoss += spread
        maxLoss = min(maxLoss,spread)
        nLoss +=1
        lLoss.append(spread)

avgWin = totalWin/nWin
avgLoss = totalLoss/nLoss
stdWin = np.std(np.asarray(lWins))
stdLoss = np.std(np.asarray(lLoss))

fid = open('fit.out','w+')
line = '{}{}{}{}{}{}{}\n'.format(profit,totalWin,totalLoss,avgWin,avgLoss,stdWin,stdLoss)
fid.write(line)
fid.close()

if not inp['FIT']:
    print('Total balance\t{}'.format(totale))
    print('Profit = {:5.2f}% over {} periods'.format((totale - initialBalance)/initialBalance *100.,len(closes)))
    print('{} winning trades, {} losing trade'.format(nWin,nLoss))
    print('average : win {:5.2f}%, loss {:5.2f}%'.format(avgWin,avgLoss))
    print('std Win {:5.2f}%, std Loss {:5.2f}%'.format(stdWin,stdLoss))
    print('max Win {:5.2f}%, max Loss {:5.2f}%'.format(maxWin,maxLoss))

    #########
    # Plots #
    #########

    buys = []
    buyDate = []
    sells = []
    sellDate = []


    for i in range(len(trades)):
        if trades[i][-1] == 'buy':
            buys.append(trades[i][1])
            buyDate.append(trades[i][0])
        else:
            sells.append(trades[i][1])
            sellDate.append(trades[i][0])

    #plt.rcParams["figure.figsize"] = (24,12)
    #fig, ax = plt.subplots()
    ax1 = plt.subplot2grid((9,1), (0,0), rowspan=7, colspan=1)

    txt = 'Profit = {:5.2f}%\n{} Winning trade\n{} Losing trades\naverage win = {:5.2f}%\naverage loss = {:5.2f}%\nMax Loss = {:5.2f}%'.format(profit,nWin,nLoss,avgWin,avgLoss,maxLoss)
    plt.text(min(dates)*0.2, max(closes)*0.8, txt, bbox=dict(facecolor='gray', alpha=0.5))

    candlestick_ohlc(ax1,zip(dates,opens,highs,lows,closes),width=0.6, colorup='g')
    plt.grid()
    plt.plot(dates,data.MA_20, 'r-')
    plt.plot(dates,data.MA_50, 'b-')
    plt.plot(dates,data.MA_100, 'c-')
    plt.plot(dates,data.MA_100, 'k-')
    plt.plot(dates,data.PSAR, 'k:')
    #plt.plot(dates,data.KCU_20, 'b--')
    #plt.plot(dates,data.KCD_20, 'b--')
    #plt.plot(dates,data.BBU_20, 'c--')
    #plt.plot(dates,data.BBD_20, 'c--')

    plt.plot(buyDate,buys, 'k^', lw = 10)
    plt.plot(sellDate,sells, 'kv', lw = 10)

    """
    plt.plot(dates,Ind['BBU'], 'b-')
    plt.plot(dates,Ind['BBD'], 'b-')
    plt.plot(dates,Ind['KCU'], 'b-')
    plt.plot(dates,Ind['KCD'], 'b-')
    plt.plot(dates,Ind['MA20'], 'r-')
    plt.plot(dates,Ind['MA100'], 'g:')
    plt.plot(dates,Ind['BBMA'], 'b-')
    plt.plot(dates,Ind['PSAR'], 'k.')
    """

    axy = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    axy.set_ylabel('balance USD', )  # we already handled the x-label with ax1
    axy.plot(dates, balance, 'k-', )
    axy.tick_params(axis='y', )

    """
    ax2 = plt.subplot2grid((9,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
    plt.grid()
    ax2.plot(dates,data.MACDl_1226)
    ax2.plot(dates,data.MACDs_1226)
    ax2.fill_between(dates,data.MACDh_1226)

    ax3 = plt.subplot2grid((9,1), (6,0), rowspan=1, colspan=1, sharex=ax1)
    plt.grid()
    ax3.plot(dates,data.SORSI_14k3, 'r-')
    ax3.plot(dates,data.SORSI_14d33, 'c-')
    ax3.plot(dates,data.RSI_14, 'b-')
    ax3.axhline( y = 70, ls = ':', c = 'b')
    ax3.axhline( y = 30, ls = ':', c = 'b')

    ax4 = plt.subplot2grid((9,1), (7,0), rowspan=1, colspan=1, sharex=ax1)
    plt.grid()
    ax4.plot(dates,Signal)


    ax5 = plt.subplot2grid((9,1), (8,0), rowspan=1, colspan=1, sharex=ax1)
    plt.grid()
    ax5.plot(dates,devSignal)
    """

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()
    plt.savefig('BotStat.png', dpi=600)
