from time import sleep
import SRC.lib.observer as observer

class MasterBot:
    def __init__(self,masterScreener):
        self.bots = []
        self.masterScreener = masterScreener

    def add_bot(self,strategy, api, pair, timeframe):
        bot = Bot(strategy, api, pair, timeframe)
        self.bots.append(bot)

    def find_bot(self, strategy, api, pair, timeframe):
        for bot in self.bots:
            if bot.strategy == strategy and bot.api == api and bot.pair == pair and bot.timeframe == timeframe:
                return bot
        return None
    
    def get_bot(self, strategy, api, pair, timeframe):
        bot = self.find_bot(strategy, api, pair, timeframe)
        if bot:
            return bot
        else:
            self.add_bot(strategy, api, pair, timeframe)
            bot = self.find_bot( strategy, api, pair, timeframe)
            screneer = self.masterScreener.get_screener(pair, timeframe, api)
            screneer.attach(bot)
            return bot

class Bot(observer.Observer):
    def __init__(self, strategy, api, pair, timeframe):
        self.strategy = strategy
        self.api = api
        self.pair = pair
        self.timeframe = timeframe
        self.running = False
        print(f"Bot initialized with strategy {self.strategy.name} on pair {self.pair}, on timeFrame {self.timeframe}, using {self.api} API.")
        
    def update(self, subject: observer.Subject) -> None:
        print(f"\tBot with strategy {self.strategy.name} on pair {self.pair}, on timeFrame {self.timeframe}, using {self.api} API is apdated with new data.")
        self.strategy.process_data(subject.get_data())
        # Here you can add logic to execute trades based on strategy signals
        if self.strategy.long:
            print(f"\tBot executing long position on {self.pair} using {self.api} API.")
        else:
            print(f"\tBot not in long position on {self.pair} using {self.api} API.")

        