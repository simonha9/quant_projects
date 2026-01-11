from datetime import datetime
import uuid

from backtester.strategy.side import Side
from backtester.portfolio.order_intent import OrderIntent

# simulates a filled trade form a validated orderintent
class FilledTrade:
    id: uuid
    instrument_id: str
    side: Side
    qty: int
    price: float
    timestamp: datetime


    def __init__(self, instrument_id: str, side: Side, qty: int, price: float):
        self.id = uuid.uuid4()
        self.instrument_id = instrument_id
        self.side = side
        self.qty = qty
        self.price = price
        self.timestamp = datetime.now()

    def get_id(self) -> uuid:
        return self.id

    def get_instrument_id(self) -> str:
        return self.instrument_id
    
    def get_side(self) -> Side:
        return self.side
    
    def get_qty(self) -> int:
        return self.qty
    
    def get_price(self) -> float:
        return self.price
    
    def get_timestamp(self) -> datetime:
        return self.timestamp

class ExecutionModel:
    def fill_trade(orderIntent: OrderIntent) -> FilledTrade:
        return FilledTrade(
            instrument_id=orderIntent.get_instrument(), 
            side=orderIntent.get_side(),
            qty=orderIntent.get_qty(),
            price=orderIntent.get_mark_price()
        )
    