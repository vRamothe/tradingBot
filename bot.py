import hmac,hashlib
import urllib,json
import pprint,time
import sys, getopt
import numpy as np

import indicators

def StopLoss(highs, lows, closes, stoploss, psar, bull, inp):
    if inp['StopLossType'] == 'Fix':
        result = closes[-1] - inp['StopLossValue']
    elif inp['StopLossType'] == 'Rate':
        result = closes[-1] - ( closes[-1] * float(inp['StopLossValue'])/100.)
    elif inp['StopLossType'] == 'PSAR':
        newstop = psar[-1]
        if newstop < closes[-1]:
            result = newstop
        else:
            result = stoploss
    elif inp['StopLossType'] == False:
        result = 0
    else:
        print ('StopLossType should be \'Fix\' or \'Rate\'')
        print('StopLossValue as to be a positive number')
        sys.exit()
    return result

def update(b1,b2, opens, highs, lows, closes ,position ,stoploss ,dates ,trades ,inp ,signal, devsignal, psar, bull):
    if inp['TrailingStop'] and position == 'open' :
        stoploss = StopLoss(highs, lows, closes, stoploss, psar, bull, inp)

    if devsignal > 0 and position == 'closed' and closes[-1] > stoploss:
        position = 'open'
        b2 = b1 / closes[-1] * (1-0.0015)
        b1 = 0
        trades.append([dates[-1],closes[-1], b2*closes[-1],'buy'])
        stoploss = StopLoss(highs, lows, closes, stoploss, psar, bull, inp)

    elif (lows[-1] < stoploss or devsignal <= 0 ) and position == 'open':
        position = 'closed'
        if lows[-1] < stoploss:
            b1 = b2 * stoploss * (1-0.0015)
            b2 = 0
            trades.append([dates[-1],stoploss,b1,'stop'])
        else:
            b1 = b2 * closes[-1] * (1-0.0015)
            b2 = 0
            trades.append([dates[-1],closes[-1],b1,'close'])
        stoploss = 0

    if b1+b2 == 0:
        print('Balance Lost')
        sys.exit()
    return(b1,b2,position,stoploss,trades)

def supdate(b1,b2,prices, highs, lows, opens, closes ,position ,stoploss ,dates ,trades ,inp ,signal,psar, bull):
    trade = signal
    norm = 11
    b2target = 0.5 * (1-np.cos(np.pi*trade/norm))
    if b2target < 0:
        b2target = 0
    b1target = 1-b2target
    btot = b1+b2 * closes[-1]
    psar,bull = indicators.PSAR(highs,lows,closes)
    if inp['TrailingStop'] and position == 'open' :
        stoploss = StopLoss(prices, highs, lows, closes, stoploss, psar, bull, inp)

    if trade > 0 :
        position = 'open'
        b2 = btot * b2target / closes[-1] #* (1-0.0015)
        b1 = btot * b1target
        trades.append([dates[-1],closes[-1],'buy'])
        stoploss = StopLoss(prices, highs, lows, closes, stoploss, psar, bull, inp)

    if closes[-1] < stoploss or trade <= 0 and position == 'open':
        position = 'closed'
        if closes[-1] <= stoploss:
            b1 += b2 * stoploss #* (1-0.0015)
            b2 = 0
            trades.append([dates[-1],stoploss,'close'])
        else:
            b1 += b2 * closes[-1] #* (1-0.0015)
            b2 = 0
            trades.append([dates[-1],closes[-1],'close'])

        stoploss = 0

    if b1+b2 == 0:
        print('Balance Lost')
        sys.exit()
    return(b1,b2,position,stoploss,trades)
