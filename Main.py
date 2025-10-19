
import signal
import os

# Handle KeyboardInterrupt to stop all object instance gracefully
def signal_handler(sig, frame):
    print("\n Program aborting by system handles KeyboardInterrupt (CTRL+C) ...")
    master.master_screener.stop_all()
    os._exit(0)
signal.signal(signal.SIGINT, signal_handler)

import SRC.utils as utilitys
import SRC.bot as bot
import SRC.screener as screener
import SRC.lib.strategie as strategie

from time import sleep

class Master():
    def __init__(self):
        self.master_screener = screener.MasterScreener()
        self.master_bot = bot.MasterBot(self.master_screener)
        

master = Master()

if __name__ == "__main__":
    print('Screener module test')
    master.master_screener.add_screener('BTCUSDT', '1m', 'binance')
    # master.master_screener.add_screener('ETHUSDT', '1m', 'binance')
    testBot = master.master_bot.get_bot(strategie.SMAStrategy(), 'binance', 'BTCUSDT', '1m')

    # Keep the main thread alive to allow background threads to run
    while True:
        sleep(1) 