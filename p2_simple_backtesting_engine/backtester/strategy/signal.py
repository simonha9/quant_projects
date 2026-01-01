from datetime import datetime
from backtester.strategy.side import Side
from backtester.strategy.strategy_type import StrategyType


# Signal class
class Signal:
    instrument_id: str
    side: Side
    signal_type: StrategyType
    confidence: float
    timestamp: datetime

    def __init__(
        self,
        instrument_id: str,
        side: Side,
        signal_type: StrategyType,
        timestamp: datetime,
        confidence: float = None
    ):
        self.instrument_id = instrument_id
        self.side = side
        self.signal_type = signal_type
        self.timestamp = timestamp
        self.confidence = confidence

