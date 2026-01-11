import pandas as pd
from datetime import datetime
from unittest.mock import MagicMock

from backtester.portfolio.portfolio_manager import PortfolioManager
from backtester.portfolio.constraints import ConstraintResult
from backtester.portfolio.order_intent import OrderIntent, Side


# -------------------------------------------------
# Mocks / Test Doubles
# -------------------------------------------------

class MockPosition:
    def __init__(self, qty=0):
        self._qty = qty

    def get_qty(self):
        return self._qty


class MockPositionManager:
    def find_position_by_instrument_id(self, instrument_id):
        return MockPosition(0)

    def get_total_position_equity(self):
        return 0.0


class MockExecutionModel:
    def __init__(self):
        self.called = 0

    def fill_trade(self):
        self.called += 1
        return MagicMock()  # fake FilledTrade


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def make_portfolio_manager(cash=10_000):
    pm = PortfolioManager(
        data=pd.DataFrame(),
        position_manager=MockPositionManager(),
        execution_model=MockExecutionModel(),
    )

    pm.cash = cash
    pm.ledger = MagicMock()
    return pm


# -------------------------------------------------
# Tests
# -------------------------------------------------

def test_handle_order_intents_executes_and_records_trade():
    pm = make_portfolio_manager()

    # Force constraints to allow the trade
    pm.validate_constraints = MagicMock(
        return_value=ConstraintResult(
            instrument_id="AAPL",
            allowed=True,
        )
    )

    intent = OrderIntent(
        instrument_id="AAPL",
        side=Side.BUY,
        qty=10,
        price=100,
        timestamp=datetime.now(),
        intent_type=None,
    )

    pm.handle_order_intents([intent])

    # Execution happened once
    assert pm.execution_model.called == 1

    # Ledger received one filled trade
    pm.ledger.process_filled_orders.assert_called_once()
    filled_orders = pm.ledger.process_filled_orders.call_args[0][0]
    assert len(filled_orders) == 1


def test_handle_order_intents_rejected_order_not_executed():
    pm = make_portfolio_manager()

    # Force constraint failure
    pm.validate_constraints = MagicMock(
        return_value=ConstraintResult(
            instrument_id="AAPL",
            allowed=False,
            reason="blocked",
        )
    )

    intent = OrderIntent(
        instrument_id="AAPL",
        side=Side.BUY,
        qty=10,
        price=100,
        timestamp=datetime.now(),
        intent_type=None,
    )

    pm.handle_order_intents([intent])

    # No execution
    assert pm.execution_model.called == 0

    # Ledger still called, but with empty list
    pm.ledger.process_filled_orders.assert_called_once_with([])


def test_multiple_order_intents_partial_fill():
    pm = make_portfolio_manager()

    # First allowed, second rejected
    pm.validate_constraints = MagicMock(
        side_effect=[
            ConstraintResult("AAPL", allowed=True),
            ConstraintResult("TSLA", allowed=False, reason="blocked"),
        ]
    )

    intents = [
        OrderIntent(
            instrument_id="AAPL",
            side=Side.BUY,
            qty=5,
            price=100,
            timestamp=datetime.now(),
            intent_type=None,
        ),
        OrderIntent(
            instrument_id="TSLA",
            side=Side.BUY,
            qty=5,
            price=200,
            timestamp=datetime.now(),
            intent_type=None,
        ),
    ]

    pm.handle_order_intents(intents)

    assert pm.execution_model.called == 1

    filled_orders = pm.ledger.process_filled_orders.call_args[0][0]
    assert len(filled_orders) == 1


def test_total_portfolio_value_uses_cash_and_positions():
    pm = make_portfolio_manager(cash=5_000)

    total_value = pm.get_total_portfolio_value()

    assert total_value == 5_000
