import sys, getopt
from botchart import BotChart
from botstrategy import BotStrategy

def main(argv):
	chart = BotChart(argv[0],argv[1],argv[2])

	strategy = BotStrategy()

	for candlestick in chart.getPoints():
		strategy.tick(candlestick)

if __name__ == "__main__":
	main(sys.argv[1:])
