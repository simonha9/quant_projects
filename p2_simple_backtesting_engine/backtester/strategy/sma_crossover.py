from datetime import datetime
from backtester.strategy.strategy import Strategy
from backtester.strategy.signal import Signal, Side, StrategyType
import pandas as pd

# This is a super basic SMA crossover implementation
# We will use the common 50,200 and look for intersections

class SMACrossover(Strategy):
    instrument_id: str

    def __init__(self, instrument_id: str):
        self.instrument_id = instrument_id

    def execute(self, data: pd.DataFrame) -> list[Signal]:
        signals = []

        # get the 50 SMA
        data['SMA_50'] = data['close'].rolling(window=50).mean()
        # get the 200 SMA
        data['SMA_200'] = data['close'].rolling(window=200).mean()

        # When do they intersect?
        # They intersect when :
        # SMA_50 was below SMA_200 and now is going above
        #   in this case, we should buy
        # SMA_50 was above SMA_200 and now is going below
        #   in this case, we should sell

        # We definitely want to cache this
        prev_sma_50 = data['SMA_50'].shift(1)
        prev_sma_200 = data['SMA_200'].shift(1)

        # bitmask it and iterate to append signals
        cross_up = (prev_sma_50 <= prev_sma_200) & (data['SMA_50'] > data['SMA_200'])
        cross_down = (prev_sma_50 > prev_sma_200) & (data['SMA_50'] < data['SMA_200'])

        # we only want to generate 1 signal per crossover event though, let's make it easy on us
        cross_up_event = cross_up & (~cross_up.shift(1).fillna(False))
        cross_down_event = cross_down & (~cross_down.shift(1).fillna(False))

        print(data[['SMA_50', 'SMA_200']].tail(10))

        for idx in data.index[cross_up_event]:
            # Buy
            signals.append(Signal(
                instrument_id=self.instrument_id, 
                direction=Side.BUY, 
                signal_type=StrategyType.SMA_CROSSOVER, 
                timestamp=datetime.now()
            ))
        for idx in data.index[cross_down_event]:
            # Sell
            signals.append(Signal(
                instrument_id=self.instrument_id, 
                direction=Side.SELL, 
                signal_type=StrategyType.SMA_CROSSOVER, 
                timestamp=datetime.now()
            ))

        return signals


