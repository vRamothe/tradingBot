import os
import numpy as np
import sys
##################
# User Interface #
##################
fid = open('output.dat','r')
trig = 0
for line in fid:
	temp = line.split()
	if float(temp[-1]) > trig:
		trig  = float(temp[-1])
		nfast = temp[0]
		nslow = temp[1] 	
		delay = temp[2]	
		sl = temp[3]
		balance = temp[4]
print(nfast,nslow,delay,sl,balance)
fid.close()
