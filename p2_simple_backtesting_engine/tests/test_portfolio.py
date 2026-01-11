import pytest
import pandas as pd
from datetime import datetime

from backtester.portfolio.portfolio_manager import PortfolioManager
from backtester.portfolio.constraints import PER_INSTRUMENT_EXPOSURE_CAP_PERCENTAGE
from backtester.portfolio.order_intent import OrderIntent, Side


# -------------------------------
# Mocks
# -------------------------------

class MockPosition:
    def __init__(self, qty):
        self._qty = qty

    def get_qty(self):
        return self._qty


class MockPositionManager:
    def __init__(self, positions):
        self.positions = positions

    def find_position_by_instrument_id(self, instrument_id):
        return self.positions.get(instrument_id, MockPosition(0))

    def get_total_position_equity(self):
        return 0.0


class MockExecutionModel:
    def fill_trade(self):
        raise RuntimeError("Should not be called in constraint tests")


# -------------------------------
# Helpers
# -------------------------------

def make_pm(cash, total_value, positions):
    pm = PortfolioManager(
        data=pd.DataFrame(),
        position_manager=MockPositionManager(positions),
        execution_model=MockExecutionModel(),
    )
    pm.cash = cash

    # override total portfolio value deterministically
    pm.get_total_portfolio_value = lambda: total_value
    return pm


# -------------------------------
# Tests
# -------------------------------

def test_cash_constraint_fail():
    pm = make_pm(cash=1000, total_value=5000, positions={"AAPL": MockPosition(10)})

    intent = OrderIntent(
        instrument_id="AAPL",
        side=Side.BUY,
        qty=20,   # 20 * 100 = 2000 > cash
        price=100,
        timestamp=datetime.now(),
        intent_type=None,
    )

    result = pm.validate_constraints(pm.position_manager, intent)

    assert not result.allowed
    assert "available cash" in result.reason.lower()


def test_position_existence_fail():
    pm = make_pm(cash=10000, total_value=20000, positions={"AAPL": MockPosition(5)})

    intent = OrderIntent(
        instrument_id="AAPL",
        side=Side.SELL,
        qty=10,
        price=100,
        timestamp=datetime.now(),
        intent_type=None,
    )

    result = pm.validate_constraints(pm.position_manager, intent)

    assert not result.allowed
    assert "exceeds current position qty" in result.reason.lower()


def test_max_exposure_fail():
    pm = make_pm(
        cash=10000,
        total_value=100000,
        positions={"AAPL": MockPosition(700)},
    )

    intent = OrderIntent(
        instrument_id="AAPL",
        side=Side.BUY,
        qty=100,
        price=10,
        timestamp=datetime.now(),
        intent_type=None,
    )

    intent.get_mark_price = lambda: 10

    result = pm.validate_constraints(pm.position_manager, intent)

    assert not result.allowed
    assert "exposure" in result.reason.lower()
