import uuid
from datetime import datetime

from backtester.portfolio.ledger import Ledger
from backtester.strategy.side import Side


class FakeFilledTrade:
    def __init__(self):
        self._id = uuid.uuid4()
        self._instrument_id = "AAPL"
        self._side = Side.BUY
        self._qty = 10
        self._price = 150.0
        self._timestamp = datetime(2025, 1, 1)

    def get_id(self):
        return self._id

    def get_instrument_id(self):
        return self._instrument_id

    def get_side(self):
        return self._side

    def get_qty(self):
        return self._qty

    def get_price(self):
        return self._price

    def get_timestamp(self):
        return self._timestamp


def test_add_record_creates_ledger_record():
    ledger = Ledger()
    filled_trade = FakeFilledTrade()

    ledger.add_record(filled_trade)

    assert len(ledger.records) == 1
    record = ledger.records[0]

    assert record.instrument_id == "AAPL"
    assert record.side == Side.BUY
    assert record.qty == 10
    assert record.price == 150.0
    assert record.timestamp == filled_trade.get_timestamp()
    assert record.filled_trade_id == filled_trade.get_id()


def test_process_filled_orders_adds_multiple_records():
    ledger = Ledger()
    trades = [FakeFilledTrade(), FakeFilledTrade()]

    ledger.process_filled_orders(trades)

    assert len(ledger.records) == 2
