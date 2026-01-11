import pandas as pd
from backtester.portfolio.position_manager import PositionManager
from backtester.portfolio.order_intent import OrderIntent
from backtester.portfolio.execution_model import ExecutionModel
from backtester.portfolio.ledger import Ledger
from backtester.portfolio.constraints import ConstraintResult, PER_INSTRUMENT_EXPOSURE_CAP_PERCENTAGE


# This is the meat of the portfolio manager, it should manage the actual flow detailed in the readme.
class PortfolioManager:
    data: pd.DataFrame
    cash: float
    position_manager: PositionManager
    execution_model: ExecutionModel
    ledger: Ledger


    def __init__(self, data: pd.DataFrame, position_manager: PositionManager, execution_model: ExecutionModel):
        self.data = data
        self.position_manager = position_manager
        self.execution_model = execution_model


    def add_cash(self, cash_to_add: float) -> float:
        self.cash += cash_to_add
        return self.cash

    def subtract_cash(self, cash_to_subtract: float) -> float:
        self.cash -= cash_to_subtract
        return self.cash

    def get_available_cash(self) -> float:
        return self.cash
    
    def get_total_portfolio_value(self) -> float:
        return self.position_manager.get_total_position_equity() + self.cash
    
    def handle_order_intents(self, order_intents: list[OrderIntent]) -> None:
        filled_orders = []
        for order_intent in order_intents:
            constraint_result = self.validate_constraints(self.position_manager, order_intent)
            if constraint_result.is_allowed():
                filled_orders.append(self.execution_model.fill_trade())
        
        self.ledger.process_filled_orders(filled_orders)
           

    # below are some very constraints that our portfolio manager needs to abide by

    # cash constraint: the price of the position cannot be more than our current cash
    # position existence: you have to own the position you are trying to sell
    # max position size: cap per-instrument exposure so you diversify (like <= 2%)
    # no leverage: cap total exposure <= portfolio value (don't go into debt)
    # single side: don't go long + short on the same instrument
    # min trade size: ignore tiny trades (noise)

    def validate_constraints(self, positionManager: PositionManager, orderIntent: OrderIntent) -> ConstraintResult:
        position = positionManager.find_position_by_instrument_id(orderIntent.get_instrument())

        # cash constraint
        if orderIntent.is_buy_order() and orderIntent.get_total_value() > self.get_available_cash():
            return ConstraintResult(instrument_id=orderIntent.get_instrument(), allowed=False, reason="Total order value cannot exceed available cash.")
        
        # position existence
        if orderIntent.is_sell_order() and position.get_qty() < orderIntent.get_qty():
            return ConstraintResult(instrument_id=orderIntent.get_instrument(), allowed=False, reason="Total qty of order exceeds current position qty.")

        # max position exposure size
        if abs((position.get_qty() + orderIntent.get_qty()) * orderIntent.get_mark_price()) > PER_INSTRUMENT_EXPOSURE_CAP_PERCENTAGE * self.get_total_portfolio_value():
            return ConstraintResult(instrument_id=orderIntent.get_instrument(), allowed=False, reason="Total position exposure exceeds the maximum per-instrument exposure.")

        return ConstraintResult(instrument_id=orderIntent.get_instrument(), allowed=True)