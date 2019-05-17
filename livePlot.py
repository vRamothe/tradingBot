import matplotlib.pyplot as plt
import math

def livePlot(x,y, fig, ax):
    t=len(y)
    print(len(y))
    ax.plot(x, y, color = 'tab:blue')
    #plt.pause(0.01)
    print('ok')
    return(fig,ax)

"""
x = range(100)
y = range(100)
fig, ax = plt.subplots()
for i in range(len(y)):    
    fig,ax = livePlot(x[:i],y[:i],fig,ax)
    plt.pause(0.01)
"""
