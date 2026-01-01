import pandas as pd
from backtester.portfolio.position_manager import PositionManager

# This is the meat of the portfolio manager, it should manage the actual flow detailed in the readme.

class PortfolioManager:
    data: pd.DataFrame
    cash: float
    positionManager: PositionManager


    def __init__(self, data: pd.DataFrame):
        self.data = data

    def add_cash(self, cash_to_add: float) -> float:
        self.cash += cash_to_add
        return self.cash

    def subtract_cash(self, cash_to_subtract: float) -> float:
        self.cash -= cash_to_subtract
        return self.cash

    def get_available_cash(self) -> float:
        return self.cash
    
    def get_total_portfolio_value(self) -> float:
        return self.positionManager.get_total_position_equity() + self.cash
    
