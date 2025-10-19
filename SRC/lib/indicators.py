import pandas as pd
import numpy as np


def SMA(df, n):
    """Calculate the moving average for the given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    MA = pd.Series(df['close'].rolling(n, min_periods=n).mean(), name='MA_' + str(n))
    df = df.join(MA)
    return df


def EMA(df, n):
    """
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    EMA = pd.Series(df['close'].ewm(span=n, min_periods=n).mean(), name='EMA_' + str(n))
    df = df.join(EMA)
    return df


def MOMENTUM(df, n):
    """
    
    :param df: pandas.DataFrame 
    :param n: 
    :return: pandas.DataFrame
    """
    M = pd.Series(df['close'].diff(n), name='Momentum_' + str(n))
    df = df.join(M)
    return df


def ROC(df, n):
    """
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    M = df['close'].diff(n)
    N = df['close'].shift(n)
    ROC = pd.Series(100*M / N, name='ROC_' + str(n))
    df = df.join(ROC)
    return df


def ATRS(df, n):
    """
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    i = 0
    TR_l = [0]
    while i < df.index[-1]:
        TR = max(df.loc[i + 1, 'high'], df.loc[i, 'close']) - min(df.loc[i + 1, 'low'], df.loc[i, 'close'])
        TR_l.append(TR)
        i = i + 1
    TR_s = pd.Series(TR_l)
    ATR = pd.Series(TR_s.rolling(window=n, center=False).mean()  , name='ATRS_' + str(n))
    df = df.join(ATR)
    return df

def ATRE(df, n):
    """
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    i = 0
    TR_l = [0]
    while i < df.index[-1]:
        TR = max(df.loc[i + 1, 'high'], df.loc[i, 'close']) - min(df.loc[i + 1, 'low'], df.loc[i, 'close'])
        TR_l.append(TR)
        i = i + 1
    TR_s = pd.Series(TR_l)
    ATR = pd.Series(TR_s.ewm(span=n, min_periods=n).mean(), name='ATRE_' + str(n))
    df = df.join(ATR)
    return df


def BB(df, n, m):
    """
    
    :param df: pandas.DataFrame
    :param n: period
    :param m: multiplier
    :return: pandas.DataFrame
    """
    MA = pd.Series(df['close'].rolling(n, min_periods=n).mean())
    MSD = pd.Series(df['close'].rolling(n, min_periods=n).std())
    bup = MA + m * MSD
    Bup = pd.Series(bup, name='BBU_' + str(n))
    df = df.join(Bup)
    bdown = MA - m * MSD
    Bdown = pd.Series(bdown, name='BBD_' + str(n))
    df = df.join(Bdown)
    b2 = (df['close'] - bdown) / (bup - bdown)
    B2 = pd.Series(b2, name='BBp_' + str(n))
    df = df.join(B2)
    return df


def PPSR(df):
    """Calculate Pivot Points, Supports and Resistances for given data
    
    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """
    PP = pd.Series((df['high'] + df['low'] + df['close']) / 3)
    R1 = pd.Series(2 * PP - df['low'])
    S1 = pd.Series(2 * PP - df['high'])
    R2 = pd.Series(PP + df['high'] - df['low'])
    S2 = pd.Series(PP - df['high'] + df['low'])
    R3 = pd.Series(df['high'] + 2 * (PP - df['low']))
    S3 = pd.Series(df['low'] - 2 * (df['high'] - PP))
    psr = {'PP': PP, 'R1': R1, 'S1': S1, 'R2': R2, 'S2': S2, 'R3': R3, 'S3': S3}
    PSR = pd.DataFrame(psr)
    df = df.join(PSR)
    return df

def STOCHASTIC(df,n,nk,nd):
    """Calculate stochastic oscillator %K for given data.
    
    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    Stoch = pd.Series(100*(df['close'] - df['low']) / (df['high'] - df['low']), name= 'Stochastic_'+str(n))
    k = pd.Series(Stoch.ewm(span=nk, min_periods=nk).mean(), name='StochasticK_' + str(n) + '_' + str(nk))
    d = pd.Series(k.ewm(span=nk, min_periods=nk).mean(), name='StochasticD_' + str(n)+ '_' + str(nk) + '_' + str(nd))
    df = df.join(Stoch)
    df = df.join(k)
    df = df.join(d)    
    return df

def STOS(df, n, nK, nD):  
    SOk = pd.Series(100*(df['close'] - df['low'].rolling(n).min()) / (df['high'].rolling(n).max() - df['low'].rolling(n).min()), name = 'SOk'+str(n)+str(nK))  
    SOd = pd.Series(SOk.ewm(ignore_na=False, span=nD, min_periods=nD-1, adjust=True).mean(), name = 'SOd'+str(n)+str(nK)+str(nD))  
    SOk = SOk.rolling(window=nK, center=False).mean()  
    SOd = SOd.rolling(window=nD, center=False).mean()  
    df = df.join(SOk)  
    df = df.join(SOd)  
    return df

def STOE(df, n, nK, nD):  
    SOk = pd.Series(100*(df['close'] - df['low'].rolling(n).min()) / (df['high'].rolling(n).max() - df['low'].rolling(n).min()), name = 'SOk'+str(n)+str(nK))  
    SOd = pd.Series(SOk.ewm(ignore_na=False, span=nD, min_periods=nD-1, adjust=True).mean(), name = 'SOd'+str(nK)+str(nD))  
    SOk = SOk.ewm(ignore_na=False, span=nS, min_periods=nS-1, adjust=True).mean()  
    SOd = SOd.ewm(ignore_na=False, span=nS, min_periods=nS-1, adjust=True).mean()  
    df = df.join(SOk)  
    df = df.join(SOd)  
    return df  

def STORSIS(df,n,nK,nD):
    """Calculate stochastic oscillator %K for given data.
    
    :param df1, df2,df3: pandas.DataFrame high, low,close or rsi,rsi,rsi
    :return: pandas.DataFrame
    """
    label = 'RSI_' + str(n)
    SOk = pd.Series(100*(df[label] - df[label].rolling(n).min()) / (df[label].rolling(n).max() - df[label].rolling(n).min()), name = 'SO'+ label + 'k'+str(nK))  
    SOd = pd.Series(SOk.ewm(ignore_na=False, span=nD, min_periods=nD-1, adjust=True).mean(), name = 'SO'+ label +'d'+str(nK)+str(nD))  
    SOk = SOk.rolling(window=nK, center=False).mean()  
    SOd = SOd.rolling(window=nD, center=False).mean()  
    df = df.join(SOk)  
    df = df.join(SOd)  
    return df

def STORSIE(df,n,nK,nD):
    """Calculate stochastic oscillator %K for given data.
    
    :param df1, df2,df3: pandas.DataFrame high, low,close or rsi,rsi,rsi
    :return: pandas.DataFrame
    """
    SOk = pd.Series(100*(df[label] - df[label].rolling(n).min()) / (df[label].rolling(n).max() - df[label].rolling(n).min()), name = 'SO'+ label + 'k'+str(nK)+str(nD))  
    SOd = pd.Series(SOk.ewm(ignore_na=False, span=nD, min_periods=nD-1, adjust=True).mean(), name = 'SO'+ label +'d'+str(n)+str(nK)+str(nD))    
    SOk = SOk.rolling(window=nK, center=False).mean()  
    SOd = SOd.rolling(window=nD, center=False).mean()  
    df = df.join(SOk)  
    df = df.join(SOd)  
    return df

def TRIX(df, n):
    """Calculate TRIX for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    EX1 = df['close'].ewm(span=n, min_periods=n).mean()
    EX2 = EX1.ewm(span=n, min_periods=n).mean()
    EX3 = EX2.ewm(span=n, min_periods=n).mean()
    i = 0
    ROC_l = [np.nan]
    while i + 1 <= df.index[-1]:
        ROC = 10000*(EX3[i + 1] - EX3[i]) / EX3[i]
        ROC_l.append(ROC)
        i = i + 1
    Trix = pd.Series(ROC_l, name='Trix_' + str(n))
    df = df.join(Trix)
    return df


def MACD(df, n_fast, n_slow):
    """Calculate MACD, MACD Signal and MACD difference
    
    :param df: pandas.DataFrame
    :param n_fast: 
    :param n_slow: 
    :return: pandas.DataFrame
    """
    EMAfast = pd.Series(df['close'].ewm(span=n_fast, min_periods=n_slow).mean())
    EMAslow = pd.Series(df['close'].ewm(span=n_slow, min_periods=n_slow).mean())
    MACD = pd.Series(EMAfast - EMAslow, name='MACDl_' + str(n_fast) + str(n_slow))
    MACDsign = pd.Series(MACD.ewm(span=9, min_periods=9).mean(), name='MACDs_' + str(n_fast) + str(n_slow))
    MACDdiff = pd.Series(MACD - MACDsign, name='MACDh_' + str(n_fast) + str(n_slow))
    df = df.join(MACD)
    df = df.join(MACDsign)
    df = df.join(MACDdiff)
    return df

def RSI(df, period=14):
    """Calculate Relative Strength Index(RSI) for given data.

    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    # wilder's RSI
    column="close"
    delta = df[column].diff()
    up, down = delta.copy(), delta.copy()

    up[up < 0] = 0
    down[down > 0] = 0

    rUp = up.ewm(com=period - 1,  adjust=False).mean()
    rDown = down.ewm(com=period - 1, adjust=False).mean().abs()

    rsi = 100 - 100 / (1 + rUp / rDown)   

    return df.join(rsi.to_frame('RSI_'+str(period)))

def CHAIKINocs(df):
    """Calculate Chaikin Oscillator for given data.
    
    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """
    ad = (2 * df['close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']
    ad = ad.rolling(2).sum()
    Chaikin = pd.Series(ad.ewm(span=3, min_periods=3).mean() - ad.ewm(span=10, min_periods=10).mean(), name='ChaikinOSC')
    df = df.join(Chaikin)
    return df

def CHAIKINmf(df):
    """Calculate Chaikin Oscillator for given data.
    
    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """
    ad = (2 * df['close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']
    mf = ad.rolling(21).sum()
    mv = df['volume'].rolling(21).sum()
    Chaikin = pd.Series( mf / mv , name='ChaikinMF')
    df = df.join(Chaikin)
    return df

def MONEYFLOW(df, n):
    """Calculate Money Flow Index and Ratio for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    PP = (df['high'] + df['low'] + df['close']) / 3
    i = 0
    PosMF = [0]
    NegMF = [0]
    while i < df.index[-1]:
        if PP[i + 1] > PP[i]:
            PosMF.append(PP[i + 1] * df.loc[i + 1, 'volume'])
            NegMF.append(0)
        else:
            NegMF.append(PP[i + 1] * df.loc[i + 1, 'volume'])
            PosMF.append(0)
        i = i + 1
    PosMF = pd.Series(PosMF).rolling(n).sum()
    NegMF = pd.Series(NegMF).rolling(n).sum()
    MFR = pd.Series(100 - 100 / ( 1 + PosMF/NegMF))
    MFI = pd.Series(MFR, name='MFI_' + str(n))
#    MFI = pd.Series(MFR.rolling(n, min_periods=n).mean(), name='MFI_' + str(n))
    df = df.join(MFI)
    return df


def OBV(df, n):
    """Calculate On-Balance Volume for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    i = 0
    OBV = [0]
    while i < df.index[-1]:
        if df.loc[i + 1, 'close'] - df.loc[i, 'close'] > 0:
            OBV.append(df.loc[i + 1, 'volume'])
        if df.loc[i + 1, 'close'] - df.loc[i, 'close'] == 0:
            OBV.append(0)
        if df.loc[i + 1, 'close'] - df.loc[i, 'close'] < 0:
            OBV.append(-df.loc[i + 1, 'volume'])
        i = i + 1
    OBV = pd.Series(OBV)
    OBV_ma = pd.Series(OBV.rolling(n, min_periods=n).mean(), name='OBV_' + str(n))
    df = df.join(OBV_ma)
    return df

def KC(df, n, m):
    """Calculate Keltner Channel for given data.
    
    :param df: pandas.DataFrame
    :param n:
    :params m:
    :return: pandas.DataFrame
    """
    i = 0
    TR_l = [0]
    while i < df.index[-1]:
        TR = max(df.loc[i + 1, 'high'], df.loc[i, 'close']) - min(df.loc[i + 1, 'low'], df.loc[i, 'close'])
        TR_l.append(TR)
        i = i + 1
    TR_s = pd.Series(TR_l)
    ATR = pd.Series(TR_s.ewm(span=n, min_periods=n).mean(), name='ATRE_' + str(n))

    KelChM = pd.Series(((df['high'] + df['low'] + df['close']) / 3).rolling(n, min_periods=n).mean(),
                       name='KCM_' + str(n))
    KelChU = pd.Series(KelChM + m * ATR, name='KCU_' + str(n) )
    KelChD = pd.Series(KelChM - m * ATR, name='KCD_' + str(n) )
    df = df.join(KelChM)
    df = df.join(KelChU)
    df = df.join(KelChD)
    return df

def STDDEV(df, n):
    """Calculate Standard Deviation for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = df.join(pd.Series(df['Close'].rolling(n, min_periods=n).std(), name='STD_' + str(n)))
    return df

def ADL(df, n):
    """Calculate Accumulation/Distribution for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    ad = (2 * df['close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']
    M = ad.diff(n - 1)
    N = ad.shift(n - 1)
    ROC = M / N
    AD = pd.Series(ROC, name='ADLROC_' + str(n))
    df = df.join(AD)
    return df

def PSAR(df):
    def psar(high,low,close, **kwargs):
        PSARstart = kwargs.get('PSARstart',0.02)
        PSARstep = kwargs.get('PSARstep', 0.02)
        PSARmax = kwargs.get('PSARmax', 0.2)
        delta = kwargs.get('delta', 0)

        length = len(close)
        psar = close[0:len(close)]
        psarbull = [None] * length
        psarbear = [None] * length
        psartrend = [None] * length
        bull = True
        af = PSARstart
        ep = low[0]
        hp = high[0]
        lp = low[0]
        for i in range(2,length):
                if bull:
                        psar[i] = psar[i - 1] + af * (hp - psar[i - 1])
                else:
                        psar[i] = psar[i - 1] + af * (lp - psar[i - 1])
                reverse = False
                if bull:
                    if low[i] < psar[i]:
                        bull = False
                        reverse = True
                        psar[i] = hp
                        lp = low[i]
                        af = PSARstart
                else:
                    if high[i] > psar[i]:
                        bull = True
                        reverse = True
                        psar[i] = lp
                        hp = high[i]
                        af = PSARstart
                if not reverse:
                    if bull:
                        if high[i] > hp:
                            hp = high[i]
                            af = min(af + PSARstep, PSARmax)
                        if low[i - 1] < psar[i]:
                            psar[i] = low[i - 1]
                        if low[i - 2] < psar[i]:
                            psar[i] = low[i - 2]
                    else:
                        if low[i] < lp:
                            lp = low[i]
                            af = min(af + PSARstep, PSARmax)
                        if high[i - 1] > psar[i]:
                            psar[i] = high[i - 1]
                        if high[i - 2] > psar[i]:
                            psar[i] = high[i - 2]
                if bull:
                    psarbull[i] = psar[i]
                    psartrend[i] = True
                else:
                    psarbear[i] = psar[i]
                    psartrend[i] = False
        return psar , psartrend
    h = df.high.copy()
    l = df.low.copy()
    c = df.close.copy()
    psar, trend  = psar(h,l,c)
    trend [0] = trend[1] = False
    psar = pd.Series(psar, name='PSAR')
    trend = pd.Series(trend, name='PSARtrend')
    df = df.join(psar)
    df = df.join(trend)
    return df



def average_directional_movement_index(df, n, n_ADX):
    """Calculate the Average Directional Movement Index for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :param n_ADX: 
    :return: pandas.DataFrame
    """
    i = 0
    UpI = []
    DoI = []
    while i + 1 <= df.index[-1]:
        UpMove = df.loc[i + 1, 'High'] - df.loc[i, 'High']
        DoMove = df.loc[i, 'Low'] - df.loc[i + 1, 'Low']
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else:
            UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else:
            DoD = 0
        DoI.append(DoD)
        i = i + 1
    i = 0
    TR_l = [0]
    while i < df.index[-1]:
        TR = max(df.loc[i + 1, 'High'], df.loc[i, 'Close']) - min(df.loc[i + 1, 'Low'], df.loc[i, 'Close'])
        TR_l.append(TR)
        i = i + 1
    TR_s = pd.Series(TR_l)
    ATR = pd.Series(TR_s.ewm(span=n, min_periods=n).mean())
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean() / ATR)
    NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean() / ATR)
    ADX = pd.Series((abs(PosDI - NegDI) / (PosDI + NegDI)).ewm(span=n_ADX, min_periods=n_ADX).mean(),
                    name='ADX_' + str(n) + '_' + str(n_ADX))
    df = df.join(ADX)
    return df

def mass_index(df):
    """Calculate the Mass Index for given data.
    
    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """
    Range = df['High'] - df['Low']
    EX1 = Range.ewm(span=9, min_periods=9).mean()
    EX2 = EX1.ewm(span=9, min_periods=9).mean()
    Mass = EX1 / EX2
    MassI = pd.Series(Mass.rolling(25).sum(), name='Mass Index')
    df = df.join(MassI)
    return df


def vortex_indicator(df, n):
    """Calculate the Vortex Indicator for given data.
    
    Vortex Indicator described here:
        http://www.vortexindicator.com/VFX_VORTEX.PDF
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    i = 0
    TR = [0]
    while i < df.index[-1]:
        Range = max(df.loc[i + 1, 'High'], df.loc[i, 'Close']) - min(df.loc[i + 1, 'Low'], df.loc[i, 'Close'])
        TR.append(Range)
        i = i + 1
    i = 0
    VM = [0]
    while i < df.index[-1]:
        Range = abs(df.loc[i + 1, 'High'] - df.loc[i, 'Low']) - abs(df.loc[i + 1, 'Low'] - df.loc[i, 'High'])
        VM.append(Range)
        i = i + 1
    VI = pd.Series(pd.Series(VM).rolling(n).sum() / pd.Series(TR).rolling(n).sum(), name='Vortex_' + str(n))
    df = df.join(VI)
    return df


def kst_oscillator(df, r1, r2, r3, r4, n1, n2, n3, n4):
    """Calculate KST Oscillator for given data.
    
    :param df: pandas.DataFrame
    :param r1: 
    :param r2: 
    :param r3: 
    :param r4: 
    :param n1: 
    :param n2: 
    :param n3: 
    :param n4: 
    :return: pandas.DataFrame
    """
    M = df['Close'].diff(r1 - 1)
    N = df['Close'].shift(r1 - 1)
    ROC1 = M / N
    M = df['Close'].diff(r2 - 1)
    N = df['Close'].shift(r2 - 1)
    ROC2 = M / N
    M = df['Close'].diff(r3 - 1)
    N = df['Close'].shift(r3 - 1)
    ROC3 = M / N
    M = df['Close'].diff(r4 - 1)
    N = df['Close'].shift(r4 - 1)
    ROC4 = M / N
    KST = pd.Series(
        ROC1.rolling(n1).sum() + ROC2.rolling(n2).sum() * 2 + ROC3.rolling(n3).sum() * 3 + ROC4.rolling(n4).sum() * 4,
        name='KST_' + str(r1) + '_' + str(r2) + '_' + str(r3) + '_' + str(r4) + '_' + str(n1) + '_' + str(
            n2) + '_' + str(n3) + '_' + str(n4))
    df = df.join(KST)
    return df

def true_strength_index(df, r, s):
    """Calculate True Strength Index (TSI) for given data.
    
    :param df: pandas.DataFrame
    :param r: 
    :param s: 
    :return: pandas.DataFrame
    """
    M = pd.Series(df['Close'].diff(1))
    aM = abs(M)
    EMA1 = pd.Series(M.ewm(span=r, min_periods=r).mean())
    aEMA1 = pd.Series(aM.ewm(span=r, min_periods=r).mean())
    EMA2 = pd.Series(EMA1.ewm(span=s, min_periods=s).mean())
    aEMA2 = pd.Series(aEMA1.ewm(span=s, min_periods=s).mean())
    TSI = pd.Series(EMA2 / aEMA2, name='TSI_' + str(r) + '_' + str(s))
    df = df.join(TSI)
    return df


def force_index(df, n):
    """Calculate Force Index for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    F = pd.Series(df['Close'].diff(n) * df['Volume'].diff(n), name='Force_' + str(n))
    df = df.join(F)
    return df


def ease_of_movement(df, n):
    """Calculate Ease of Movement for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    EoM = (df['High'].diff(1) + df['Low'].diff(1)) * (df['High'] - df['Low']) / (2 * df['Volume'])
    Eom_ma = pd.Series(EoM.rolling(n, min_periods=n).mean(), name='EoM_' + str(n))
    df = df.join(Eom_ma)
    return df


def commodity_channel_index(df, n):
    """Calculate Commodity Channel Index for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    PP = (df['High'] + df['Low'] + df['Close']) / 3
    CCI = pd.Series((PP - PP.rolling(n, min_periods=n).mean()) / PP.rolling(n, min_periods=n).std(),
                    name='CCI_' + str(n))
    df = df.join(CCI)
    return df


def coppock_curve(df, n):
    """Calculate Coppock Curve for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    M = df['Close'].diff(int(n * 11 / 10) - 1)
    N = df['Close'].shift(int(n * 11 / 10) - 1)
    ROC1 = M / N
    M = df['Close'].diff(int(n * 14 / 10) - 1)
    N = df['Close'].shift(int(n * 14 / 10) - 1)
    ROC2 = M / N
    Copp = pd.Series((ROC1 + ROC2).ewm(span=n, min_periods=n).mean(), name='Copp_' + str(n))
    df = df.join(Copp)
    return df

def ultimate_oscillator(df):
    """Calculate Ultimate Oscillator for given data.
    
    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """
    i = 0
    TR_l = [0]
    BP_l = [0]
    while i < df.index[-1]:
        TR = max(df.loc[i + 1, 'High'], df.loc[i, 'Close']) - min(df.loc[i + 1, 'Low'], df.loc[i, 'Close'])
        TR_l.append(TR)
        BP = df.loc[i + 1, 'Close'] - min(df.loc[i + 1, 'Low'], df.loc[i, 'Close'])
        BP_l.append(BP)
        i = i + 1
    UltO = pd.Series((4 * pd.Series(BP_l).rolling(7).sum() / pd.Series(TR_l).rolling(7).sum()) + (
                2 * pd.Series(BP_l).rolling(14).sum() / pd.Series(TR_l).rolling(14).sum()) + (
                                 pd.Series(BP_l).rolling(28).sum() / pd.Series(TR_l).rolling(28).sum()),
                     name='Ultimate_Osc')
    df = df.join(UltO)
    return df


def donchian_channel(df, n):
    """Calculate donchian channel of given pandas data frame.
    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    i = 0
    dc_l = []
    while i < n - 1:
        dc_l.append(0)
        i += 1

    i = 0
    while i + n - 1 < df.index[-1]:
        dc = max(df['High'].ix[i:i + n - 1]) - min(df['Low'].ix[i:i + n - 1])
        dc_l.append(dc)
        i += 1

    donchian_chan = pd.Series(dc_l, name='Donchian_' + str(n))
    donchian_chan = donchian_chan.shift(n - 1)
    return df.join(donchian_chan)
