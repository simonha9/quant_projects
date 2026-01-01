from datetime import datetime
import uuid
from enum import Enum

from backtester.strategy.side import Side


# This is the orderIntent class, it should have:
# - instrument
# - side (buy/sell)
# - quantity
# - timestamp
# - intent_type (Entry, exit, rebalance, risk reduction, stop/liquidate)
# - reason/tag (strategy) optional
# - intent_id (unique and used for tracing)

# Enumeration of Intent types - Why are we doing what we are intending?
class Intent(Enum):
    ENTRY = 1 # I want to buy something
    EXIT = 2 # I want to sell something
    REBALANCE = 3 # I like the direction we are going but I want a different exposure
    RISK_REDUCTION = 4 # I want to reduce exposure without exiting completely
    STOP = 5 # hard stop, liquidate baby

class OrderIntent:
    order_intent_id: uuid
    instrument_id: str
    side: Side
    qty: int
    price: float
    timestamp: datetime
    intent_type: Intent
    
    def __init__(
        self,
        instrument_id: str,
        side: Side,
        qty: int,
        price: float,
        intent_type: Intent,
        timestamp: datetime | None = None,
    ):
        self.order_intent_id = uuid.uuid4()
        self.instrument_id = instrument_id
        self.side = side
        self.qty = qty
        self.price = price
        self.intent_type = intent_type
        self.timestamp = timestamp or datetime.now()

    def is_buy_order(self) -> bool:
        return self.side == Side.BUY
    
    def is_sell_order(self) -> bool:
        return self.side == Side.SELL
    
    def get_total_value(self) -> float:
        return self.qty * self.price
        
    def get_mark_price(self) -> float:
        return self.price

    def get_instrument(self) -> str:
        return self.instrument_id
    
    def get_qty(self) -> int:
        return self.qty


    