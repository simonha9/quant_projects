from enum import Enum
from abc import ABC
import pandas as pd
from backtester.strategy.signal import Signal

class Strategy(ABC):
    def execute(self, data: pd.DataFrame) -> Signal:
        """
        Executes the strategy that is currently set but must be 
        implemeneted in the subclass.  The client passes what strategy
        they want to use.
        """
        pass
