import hmac,hashlib
import urllib,urllib2,json
import pprint,time
import sys, getopt
import numpy as np

import SRC.indicators as indicators

def StopLoss(prices, highs, lows, closes, stoploss, inp):
    if inp['StopLossType'] == 'Fix':
        result = prices[-1] - inp['StopLossValue']
    elif inp['StopLossType'] == 'Rate':
        result = prices[-1] - ( prices[-1] * float(inp['StopLossValue'])/100.)
    elif inp['StopLossType'] == 'PSAR':
        newstop , bull = indicators.PSAR(highs,lows,closes)
        if bull:
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

def update(b1,b2,prices, highs, lows, opens, closes ,position ,stoploss ,dates ,trades ,inp ,signal):
    trade = sum(signal)
    psar,bull = indicators.PSAR(highs,lows,closes)
    if inp['TrailingStop'] and position == 'open' :
        stoploss = StopLoss(prices, highs, lows, closes, stoploss, inp)
            
    if trade > 0  and position == 'closed':# and bull:
        position = 'open'
        b2 = b1 / closes[-1] * (1-0.0015)
        b1 = 0
        trades.append([dates[-1],closes[-1], b2*closes[-1],'buy'])
        stoploss = StopLoss(prices, highs, lows, closes,stoploss, inp)
#        print('buy at {:10.2f}, balance is {:10.2f}'.format(closes[-1],b2*closes[-1]))

    elif (trade < 0 or closes[-1] < stoploss or not bull) and position == 'open':
#    elif (closes[-1] < stoploss or trade <0 ) and position == 'open':
        position = 'closed'
        if closes[-1] < stoploss:
            b1 = b2 * stoploss * (1-0.0015)
            b2 = 0
            trades.append([dates[-1],stoploss,b1,'close'])
#            print('stop sell at {:10.2f}, balance is {:10.2f}'.format(stoploss,b1))
        else:
            b1 = b2 * closes[-1] * (1-0.0015)
            b2 = 0
            trades.append([dates[-1],closes[-1],b1,'close'])
#            print('trade sell at {:10.2f}, balance is {:10.2f}'.format(closes[-1],b1))
        stoploss = 0
    
    if b1+b2 == 0:
        print('Balance Lost')
        sys.exit()
    return(b1,b2,position,stoploss,trades)

def supdate(b1,b2,prices, highs, lows, opens, closes ,position ,stoploss ,dates ,trades ,inp ,signal):
    trade = float(sum(signal))
    norm = float(len(signal))
    b2target = 0.5 * (1-np.cos(np.pi*trade/norm))
    if b2target < 0:
        b2target = 0
    b1target = 1-b2target
    btot = b1+b2 * closes[-1]
    psar,bull = indicators.PSAR(highs,lows,closes)
    if inp['TrailingStop'] and position == 'open' :
        stoploss = StopLoss(prices, highs, lows, closes, stoploss, inp)
            
    if trade > 0 :
        position = 'open'
        b2 = btot * b2target / closes[-1] #* (1-0.0015)
        b1 = btot * b1target
        trades.append([dates[-1],closes[-1],'buy'])
        stoploss = StopLoss(prices, highs, lows, closes,stoploss, inp)

    if closes[-1] < stoploss or trade <= 0:
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
