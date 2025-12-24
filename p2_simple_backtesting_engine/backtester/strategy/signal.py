from datetime import datetime
from enum import Enum

# Enumeration of sides
class Side(Enum):
    BUY = 1
    SELL = 2

class StrategyType(Enum):
    SMA_CROSSOVER = 1

# Signal class
class Signal:
    instrument_id: str
    direction: Side
    signal_type: StrategyType
    confidence: float
    timestamp: datetime

    def __init__(
        self,
        instrument_id: str,
        direction: Side,
        signal_type: StrategyType,
        timestamp: datetime,
        confidence: float = None
    ):
        self.instrument_id = instrument_id
        self.direction = direction
        self.signal_type = signal_type
        self.timestamp = timestamp
        self.confidence = confidence

