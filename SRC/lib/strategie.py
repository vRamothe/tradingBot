class Strategy():
    def __init__(self,name):
        self.name = name
        self.long = False
    def process_data(self, data):
        pass
    def enter_long(self):
        self.long = True
        print(f"Entering long position for strategy {self.name}")
    def exit_long(self):
        self.long = False
        print(f"Exiting long position for strategy {self.name}")

class SMAStrategy(Strategy):
    def __init__(self, short_window=5, long_window=20):
        super().__init__('SMA Strategy')
        self.short_window = short_window
        self.long_window = long_window
        self.prices = []
    def process_data(self, data):
        print(f"Processing data for SMA Strategy with short window {self.short_window} and long window {self.long_window}")
        print(f"New data received: \n{data.tail(5)}")
        self.prices.append(data['close'])
        if len(self.prices) >= self.long_window:
            short_sma = sum(self.prices[-self.short_window:]) / self.short_window
            long_sma = sum(self.prices[-self.long_window:]) / self.long_window
            if short_sma > long_sma and not self.long:
                self.enter_long()
            elif short_sma < long_sma and self.long:
                self.exit_long()