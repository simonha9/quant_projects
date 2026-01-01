from backtester.portfolio.order_intent import OrderIntent
from backtester.portfolio.position_manager import PositionManager
from backtester.portfolio.portfolio_manager import PortfolioManager

# The total exposure of an instrument cannot exceed 7.5%
PER_INSTRUMENT_EXPOSURE_CAP_PERCENTAGE = 0.075

class ConstraintResult:
    instrument_id: str
    allowed: bool
    reason: str


    def __init__(self, instrument_id: str, allowed: bool, reason: str = ""):
        self.instrument_id = instrument_id
        self.allowed = allowed
        self.reason = reason

    



# below are some very constraints that our portfolio manager needs to abide by

# cash constraint: the price of the position cannot be more than our current cash
# position existence: you have to own the position you are trying to sell
# max position size: cap per-instrument exposure so you diversify (like <= 2%)
# no leverage: cap total exposure <= portfolio value (don't go into debt)
# single side: don't go long + short on the same instrument
# min trade size: ignore tiny trades (noise)

def validate_constraints(portfolioManager: PortfolioManager, positionManager: PositionManager, orderIntent: OrderIntent) -> ConstraintResult:
    position = positionManager.find_position_by_instrument_id(orderIntent.get_instrument())


    # cash constraint
    if orderIntent.is_buy_order() and orderIntent.get_total_value() > portfolioManager.get_available_cash():
        return ConstraintResult(instrument_id=orderIntent.get_instrument(), allowed=False, reason="Total order value cannot exceed available cash.")
    
    # position existence
    if orderIntent.is_sell_order() and position.get_qty() < orderIntent.get_qty():
        return ConstraintResult(instrument_id=orderIntent.get_instrument(), allowed=False, reason="Total qty of order exceeds current position qty.")

    # max position exposure size
    if abs((position.get_qty() + orderIntent.get_qty()) * orderIntent.get_mark_price()) > PER_INSTRUMENT_EXPOSURE_CAP_PERCENTAGE * portfolioManager.get_total_portfolio_value():
        return ConstraintResult(instrument_id=orderIntent.get_instrument(), allowed=False, reason="Total position exposure exceeds the maximum per-instrument exposure.")


    return ConstraintResult(instrument_id=orderIntent.get_instrument(), allowed=True)