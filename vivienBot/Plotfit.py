import os
import numpy as np
import sys
import matplotlib.pyplot as plt
##################
# User Interface #
##################
indx = 0
indy = 2

fid = open('output.dat','r')
x = []
y = []
z = []
for line in fid:
	temp = line.split()
	if float(temp[3]) == 3 and float(temp[4]) == 0.2:
		if float(temp[indx]) not in x:
			x.append(float(temp[indx]))
		if float(temp[indy]) not in y:
			y.append(float(temp[indy]))
		z.append(float(temp[-1]))
fid.close()
print(x,y,z)
data = np.zeros((len(y),len(x)))
for i in range(len(y)):
	for j in range(len(x)):
		data[i,j] += z[i+j]


print(x,y)
plt.imshow(data, extent = (x[0],x[-1],y[0],y[-1]))
plt.colorbar(orientation='vertical')
plt.show()
