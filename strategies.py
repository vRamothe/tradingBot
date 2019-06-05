import indicators
import pandas as pd
from numpy import asarray
import FIT.fitParameters as fp

def reversal(df):
    df1 = df.shift(1)
    df2 = df
    result = df2.ge(df1).replace(True,1).replace(0,-1)
    return result

def triggerg(df, t):
    result = df.ge(t)
    result = result.replace(True,1).replace(0,-1)
    return result

def triggerl(df, t):
    result = df.le(t)
    result = result.replace(True,1).replace(0,-1)
    return result

def crossOver(df, t):
    over = df.ge(t).replace(True,1)
    cross = df.shift(1).le(t).replace(True,1)
    result = (cross*over)
    return result

def crossUnder(df, t):
    under = df.le(t).replace(True,1)
    cross = df.shift(1).ge(t).replace(True,1)
    result = (cross*under)
    return result

def overlap(df1, df2):
    result = df2.ge(df1).replace(True,1).replace(0,-1)
    return result

def Signalsprocess(df,n):
	result = []

	bull = df.PSARtrend.replace(True,1).replace(False,0)
	bear = df.PSARtrend.replace(False,1).replace(True,0)

	squeezeup = overlap(df.KCU_20,df.BBU_20).replace(-1,0)
	squeezedown = overlap(df.BBD_20,df.KCD_20).replace(-1,0)
	squeeze = (squeezeup * squeezedown).replace(0,-1)

	x00 = squeeze
	x01 = df.PSARtrend.replace(True,1).replace(False,-1)
	x02 = triggerg(df.MACDs_1226,0)
	x03 = triggerg((100-df.RSI_14),70)
	x04 = triggerg((100-df.SORSI_14k3),80)
	x05 = triggerg((100-df.SORSI_14d33),80)
	x06 = triggerg((100-df.MFI_14),80)
	x07 = triggerg((100-df.SOk143),80)
	x08 = triggerg((100-df.SOd1433),80)
	x09 = triggerg(df.RSI_14,70)
	x10 = triggerg(df.SORSI_14k3,80)
	x11 = triggerg(df.SORSI_14d33,80)
	x12 = triggerg(df.MFI_14,80)
	x13 = triggerg(df.SOk143,80)
	x14 = triggerg(df.SOd1433,80)
	x15 = triggerg(df.ROC_9,0)
	x16 = reversal(df.MACDh_1226)
	x17 = reversal(df.MA_20)
	x18 = reversal(df.MA_50)
	x19 = reversal(df.MA_100)
	x20 = reversal(df.MA_200)
	x21 = reversal(df.Trix_18)
	x22 = reversal(df.Trix_9)
	x23 = reversal(df.SORSI_14k3)
	x24 = reversal(df.SORSI_14d33)
	x25 = reversal(df.SOk143)
	x26 = reversal(df.SOd1433)
	x27 = reversal(df.Momentum_10)
	x28 = reversal(df.ROC_9)
	x29 = overlap(df.Trix_18,df.Trix_9)
	x30 = overlap(df.MA_200,df.MA_20)
	x31 = overlap(df.MA_200,df.MA_50)
	x32 = overlap(df.MA_200,df.MA_100)
	x33 = overlap(df.MA_100,df.MA_20)
	x34 = overlap(df.MA_100,df.MA_50)
	x35 = overlap(df.MA_50,df.MA_20)
	x36 = overlap(df.SORSI_14k3,df.SORSI_14d33)
	x37 = overlap(df.SOk143,df.SOd1433)
	x38 = overlap(df.MA_100,df.MA_50)
	x39 = overlap(df.MA_50,df.MA_20)

	inds = [x00,x01,x02,x03,x04,x05,x06,x07,x08,x09,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19,x20,x21,x22,x23,x24,x25,x26,x27,x28,x29,x30,x31,x32,x33,x34,x35,x36,x37,x39]

	a00 = fp.a00#                 8.6237471E+03
	a01 = fp.a01#                 6.6934229E+03
	a02 = fp.a02#                 6.5380146E+03
	a03 = fp.a03#                 3.3221814E+03
	a04 = fp.a04#                 2.9624727E+03
	a05 = fp.a05#                 7.9356207E+02
	a06 = fp.a06#                 8.7875205E+03
	a07 = fp.a07#                 5.6527178E+03
	a08 = fp.a08#                 9.2785293E+03
	a09 = fp.a09#                 2.6993169E+03
	a10 = fp.a10#                 4.6692202E+03
	a11 = fp.a11#                 4.6382866E+03
	a12 = fp.a12#                 8.8230820E+03
	a13 = fp.a13#                 3.5245022E+03
	a14 = fp.a14#                 2.0928479E+03
	a15 = fp.a15#                 4.8337188E+03
	a16 = fp.a16#                 1.9615094E+03
	a17 = fp.a17#                 2.5496133E+03
	a18 = fp.a18#                 7.1041846E+03
	a19 = fp.a19#                 1.7710026E+03
	a20 = fp.a20#                 2.2729412E+03
	a21 = fp.a21#                 8.2546758E+03
	a22 = fp.a22#                 9.0451514E+03
	a23 = fp.a23#                 7.6144592E+02
	a24 = fp.a24#                 3.0619048E+03
	a25 = fp.a25#                 4.3461588E+02
	a26 = fp.a26#                 5.6478735E+03
	a27 = fp.a27#                 2.3603185E+02
	a28 = fp.a28#                 2.1901091E+02
	a29 = fp.a29#                 7.5490527E+03
	a30 = fp.a30#                 7.4893008E+03
	a31 = fp.a31#                 9.6402002E+02
	a32 = fp.a32#                 8.0541650E+03
	a33 = fp.a33#                 7.8897388E+03
	a34 = fp.a34#                 4.7402354E+03
	a35 = fp.a35#                 9.6442100E+03
	a36 = fp.a36#                 6.9156709E+03
	a37 = fp.a37#                 7.5647539E+03
	a38 = fp.a38#                 7.6967754E+03
	a39 = fp.a39#                 8.6631582E+03

	parm1 = [a00,a01,a02,a03,a04,a05,a06,a07,a08,a09,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23,a24,a25,a26,a27,a28,a29,a30,a31,a32,a33,a34,a35,a36,a37,a39]

	for ii in range(len(parm1)):
		inds[ii] *= parm1[ii]

	p = int(fp.p)
	l = len(inds)
	result = sum(inds)
	result = result.ewm(span=p, min_periods=p).mean()
	devresult = result.diff()
	return result,devresult,l
