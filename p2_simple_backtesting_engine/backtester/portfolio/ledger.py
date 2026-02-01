from datetime import datetime
import uuid

from backtester.strategy.side import Side
from backtester.portfolio.execution_model import FilledTrade


# This is the actual record in the ledger that we record.  It is the source of truth and should
# map 1-1 to a filled_trade
class LedgerRecord:
    id: uuid
    instrument_id: str
    side: Side
    qty: int
    price: float
    timestamp: datetime
    filled_trade_id: uuid

    def __init__(self, instrument_id: str, side: Side, qty: int, price: float, timestamp: datetime, filled_trade_id: uuid):
        self.id = uuid.uuid4()
        self.instrument_id = instrument_id
        self.side = side
        self.qty = qty
        self.price = price
        self.timestamp = timestamp
        self.filled_trade_id = filled_trade_id


class Ledger:
    records: list[LedgerRecord]

    def __init__(self):
        self.records = []

    def add_record(self, filled_order: FilledTrade) -> None:
        record = LedgerRecord(
            instrument_id=filled_order.get_instrument_id(),
            side=filled_order.get_side(),
            qty=filled_order.get_qty(),
            price=filled_order.get_price(),
            timestamp=filled_order.get_timestamp(),
            filled_trade_id=filled_order.get_id()
            )
        self.records.append(record)

    def process_filled_orders(self, filled_orders: list[FilledTrade]) -> None:
        for filled_order in filled_orders:
            self.add_record(filled_order)

    def rows(self):
        return self.records