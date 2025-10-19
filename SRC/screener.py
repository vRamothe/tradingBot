from time import sleep
from SRC.utils import threaded
import SRC.lib.observer as observer

class MasterScreener:
    def __init__(self):
        self.screeners = []

    def add_screener(self, pair, timeframe, api):
        screener = Screener(pair, timeframe, api)
        self.screeners.append(screener)
        screener.monitor()

    def find_screener(self, pair, timeframe, api):
        for screener in self.screeners:
            if screener.pair == pair and screener.timeframe == timeframe and screener.api == api:
                return screener
        return None
    
    def get_screener(self, pair, timeframe, api):
        screener = self.find_screener(pair, timeframe, api)
        if screener:
            return screener
        else:
            self.add_screener(pair, timeframe, api)
            screener = self.find_screener(pair, timeframe, api)
            return screener

    def stop_all(self):
        print("Stopping all screeners...")
        for screener in self.screeners:
            screener.stop_monitoring()

class Screener(observer.Subject):
    def __init__(self, pair, timeframe, api, master=None):
        self.pair = pair
        self.timeframe = timeframe
        self.api = api
        self.api_module = apiImport(api)
        self.isMonitoring = False
        self.data = None
        self.observers = []
        print(f"Screener initialized for {self.pair} on {self.timeframe} using {self.api} API.")

    @threaded
    def monitor(self):
        self.isMonitoring = True
        print(f"Started monitoring {self.pair} on {self.timeframe} using {self.api} API.")
        while self.isMonitoring:
            data = self.fetch_data()
            self.data = self.api_module.process_data(data)
            print(f"Processed data available for {self.pair} on {self.timeframe} using {self.api} API.")
            self.notify(self)
            sleep(timeFrameToTime(self.timeframe))  # wait for a minute before the next fetch
        print(f"Stoped monitoring {self.pair} on {self.timeframe} using {self.api} API.")

    def fetch_data(self):
        print(f"Fetching data for {self.pair} on {self.timeframe} using {self.api} API.")
        return self.api_module.get_data(self.pair, self.timeframe) # Assuming each API module has a get_data function

    def store_data(self, data):
        print("Storing processed data.")
        # Placeholder for actual storage logic
        pass

    def stop_monitoring(self):
        self.isMonitoring = False

    def attach(self, observer: observer.Observer) -> None:
        print(f"Bot using strategy {observer.strategy.name}, Attached to screener {self.pair} on {self.timeframe} using {self.api} API.")
        self.observers.append(observer)

    def detach(self, observer: observer.Observer) -> None:
        print(f"Bot using strategy {observer.strategy.name}, Detached to screener {self.pair} on {self.timeframe} using {self.api} API.")
        self.observers.remove(observer)

    def notify(self, observer: observer.Observer) -> None:
        print(f"Notifying bots attached to screener {self.pair} on {self.timeframe} using {self.api} API.")
        for observer in self.observers:
            print(f"\tBot using strategy {observer.strategy.name} notified")
            observer.update(self)

    def get_data(self):
        return self.data

def timeFrameToTime(timeframe):
    mapping = {
        "1m": 60,
        "5m": 300,
        "15m": 900,
        "30m": 1800,
        "1h": 3600,
        "4h": 14400,
        "1d": 86400,
    }
    return mapping.get(timeframe, 60)  # default to 1 minute if not found

def apiImport(api_name):
    if api_name == "binance":
        from SRC.APIs import binance as api_module
    elif api_name == "kraken":
        from SRC.APIs import kraken as api_module
    elif api_name == "coinbase":
        from SRC.APIs import coinbase as api_module
    elif api_name == "bitfinex":
        from SRC.APIs import bitfinex as api_module
    elif api_name == "huobi":
        from SRC.APIs import huobi as api_module
    elif api_name == "okx":
        from SRC.APIs import okx as api_module
    elif api_name == "gateio":
        from SRC.APIs import gateio as api_module
    elif api_name == "kucoin":
        from SRC.APIs import kucoin as api_module
    elif api_name == "bittrex":
        from SRC.APIs import bittrex as api_module
    elif api_name == "poloniex":
        from SRC.APIs import poloniex as api_module
    elif api_name == "bitstamp":
        from SRC.APIs import bitstamp as api_module
    elif api_name == "alpaca":
        from SRC.APIs import alpaca as api_module
    else:
        raise ValueError(f"API '{api_name}' is not supported.")
    return api_module