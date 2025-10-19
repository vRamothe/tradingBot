#from matplotlib.finance import candlestick2_ohlc
from plotly.graph_objects import Candlestick
import matplotlib
import matplotlib.pyplot as plt

class Figure:
    def __init__(self, chartData, botData):
        self.chartData = chartData
        self.botData = botData

    def make_candlestick(self):
        self.fig = plt.figure()
        self.fig.set_size_inches(24, 12)
        self.ax1 = self.fig.add_subplot(9, 1, (1, 7))
        self.ax1.grid()
        self.ax1.set_title('Candlestick Chart')
        self.ax1.set_ylabel('Price')
        self.ax1.set_xlabel('Time')

        dates = self.chartData['dates']
        opens = self.chartData['opens']
        highs = self.chartData['highs']
        lows = self.chartData['lows']
        closes = self.chartData['closes']
        candlestick = Candlestick(x=dates, open=opens, high=highs, low=lows, close=closes)

        self.ax1.add_image(candlestick)
        ax1 = plt.subplot2grid((9,1), (0,0), rowspan=7, colspan=1)

        """
        txt = 'Profit = {:5.2f}%\n{} Winning trade\n{} Losing trades\naverage win = {:5.2f}%\naverage loss = {:5.2f}%\nMax Loss = {:5.2f}%'.format(profit,nWin,nLoss,avgWin,avgLoss,maxLoss)
        plt.text(min(dates)*0.2, max(closes)*0.8, txt, bbox=dict(facecolor='gray', alpha=0.5))
        """
        
        chartDatas  = {'dates': dates, 'opens': opens, 'highs': highs, 'lows': lows, 'closes': closes}
        ax1.add_image(Candlestick(x=chartDatas['dates'],open=chartDatas['opens'],high=chartDatas['highs'],low=chartDatas['lows'],close=chartDatas['closes']))
        
        plt.grid()
        plt.plot(dates,botData.MA_20, 'r-')
        plt.plot(dates,botData.MA_50, 'b-')
        plt.plot(dates,botData.MA_100, 'c-')
        plt.plot(dates,botData.PSAR, 'k:')
        #plt.plot(dates,botData.KCU_20, 'b--')
        #plt.plot(dates,botData.KCD_20, 'b--')
        #plt.plot(dates,botData.BBU_20, 'c--')
        #plt.plot(dates,botData.BBD_20, 'c--')

        plt.plot(botData.buyDate,botData.buys, 'k^', lw = 10)
        plt.plot(botData.sellDate,botData.sells, 'kv', lw = 10)


        axy = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        axy.set_ylabel('balance USD', )  # we already handled the x-label with ax1
        axy.plot(dates, balance, 'k-', )
        axy.tick_params(axis='y', )
        
        """
        ax2 = plt.subplot2grid((9,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
        plt.grid()
        ax2.plot(dates,chartData.MACDl_1226)
        ax2.plot(dates,chartData.MACDs_1226)
        ax2.fill_between(dates,chartData.MACDh_1226)

        ax3 = plt.subplot2grid((9,1), (6,0), rowspan=1, colspan=1, sharex=ax1)
        plt.grid()
        ax3.plot(dates,chartData.SORSI_14k3, 'r-')
        ax3.plot(dates,chartData.SORSI_14d33, 'c-')
        ax3.plot(dates,chartData.RSI_14, 'b-')
        ax3.axhline( y = 70, ls = ':', c = 'b')
        ax3.axhline( y = 30, ls = ':', c = 'b')
        """
        ax4 = plt.subplot2grid((9,1), (7,0), rowspan=1, colspan=1, sharex=ax1)
        plt.grid()
        ax4.plot(dates,botData.signal)

        ax5 = plt.subplot2grid((9,1), (8,0), rowspan=1, colspan=1, sharex=ax1)
        plt.grid()
        ax5.plot(dates,botData.devSignal)
        plt.subplots_adjust(wspace=0, hspace=0)

    def show(self):
        plt.show()
    def save(self, filename, dpi=600):
        self.fig.savefig(filename, dpi=dpi)