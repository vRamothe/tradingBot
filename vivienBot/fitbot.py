import os
import numpy as np
import sys
import hmac,hashlib
import urllib,urllib2,json
import pprint,time
import sys, getopt
from poloniex import poloniex
import datetime

##################
# User Interface #
##################
N = 1000

APIK= 'HGKS3KMW-R1DRG5CJ-MMTPHA40-JVN9DR7L'
APIS='2670d0a7345b1529bc5ea43e993708c6c0a1216370d898bca83b29f32ac7734bb1767791c16ee4311229a6fdfb6819373d513eb2fc4955730c713e8b70e32d4c'

API=poloniex(str(APIK),str(APIS))

exchange = 'poloniex'
Pair = 'USDT_BTC'
period = '14400'

endTime = int(time.time())-int(time.time())%int(period)
startTime = int(time.time())-int(time.time())%int(period)-N*int(period)
temp = API.api_query("returnChartData",{"currencyPair":Pair,"start":startTime,"end":endTime,"period":period})
print(temp[0]['open'],temp[-1]['open'])

fid = open('sample.json','w')
fid.write(json.dumps(temp, indent = 4))
fid.close()       

lnfast = range(5,25,2)
lnslow = range(30,60,2)
ldelay = range(3,15)
lsl = list(np.linspace(0.01,0.30,10))
niter = len(lnfast)*len(lnslow)*len(ldelay)*len(lsl)

os.system('rm -rf output.dat')
os.system('touch output.dat')

ii = 0
for i in lnfast:
	for k in lnslow:
		for l in ldelay:
			for m in range(len(lsl)):
				mm = lsl[m]
				bot = open('vivienBot.py','r')
				test = open('test.py','w')
				for line in bot:
					temp = line.split()
					if len(temp) == 0:
						pass
					elif len(temp) > 1 and (temp[1] == 'matplotlib.finance' or temp[1] == 'matplotlib.pyplot'):
						line = ''
					elif temp[0] == '#' and temp[1] =='Plots':
						break
					elif temp[0] == 'period':
						line = 'period = {}\n'.format(period)
					elif temp[0] == 'Pair':
						line = 'Pair = \'{}\'\n'.format(Pair)
					elif temp[0] == 'N':
						line = 'N = {}\n'.format(N)
					elif temp[0] == 'FIT':
						line = 'FIT = True\n'
					elif temp[0]=='pnfast':
						line = 'pnfast = {}\n'.format(i)
					elif temp[0]=='pnslow':
						line = 'pnslow = {}\n'.format(k)
					elif temp[0]=='pdelay':
						line = 'pdelay = {}\n'.format(l)
					elif temp[0]=='psl':
						line = 'psl = {:0.2f}\n'.format(mm)
					test.write(line)
				ii +=1
				if ii % 100 == 0 :
					print(i,k,l,mm)
					print('iteration {} sur {}'.format(ii,niter))
				test.close()
				os.system('python test.py >> output.dat')
