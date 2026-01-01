import pandas as pd
from datetime import datetime
from backtester.strategy.sma_crossover import SMACrossover
from backtester.strategy.signal import Side
from backtester.strategy.strategy_type import StrategyType


def test_sma_crossover_buy_signal():
    # Make sure the SMA windows are satisfied
    # Start with 200 bars flat, then jump 10 to trigger crossover
    close_prices = [100]*200 + [110]*10
    data = pd.DataFrame({'close': close_prices})

    strategy = SMACrossover(instrument_id="TEST")
    signals = strategy.execute(data)

    assert len(signals) == 1
    signal = signals[0]
    assert signal.side == Side.BUY
    assert signal.signal_type == StrategyType.SMA_CROSSOVER
    assert signal.instrument_id == "TEST"
    assert isinstance(signal.timestamp, datetime)


def test_sma_crossover_sell_signal():
    # SMA_50 starts above SMA_200, then drops to trigger crossover
    close_prices = [120]*50 + [110]*150 + [20]*50
    data = pd.DataFrame({'close': close_prices})

    strategy = SMACrossover(instrument_id="TEST")
    signals = strategy.execute(data)

    assert len(signals) == 1
    signal = signals[0]
    assert signal.side == Side.SELL
    assert signal.signal_type == StrategyType.SMA_CROSSOVER
    assert signal.instrument_id == "TEST"
    assert isinstance(signal.timestamp, datetime)
