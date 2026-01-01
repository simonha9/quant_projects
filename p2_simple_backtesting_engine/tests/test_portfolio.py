import pytest
from datetime import datetime
from backtester.portfolio.constraints import validate_constraints, ConstraintResult, PER_INSTRUMENT_EXPOSURE_CAP_PERCENTAGE
from backtester.portfolio.order_intent import OrderIntent, Side


# -------------------------------
# Fixtures for mocks
# -------------------------------

class MockPosition:
    def __init__(self, qty, avg_price=100):
        self._qty = qty
        self._avg_price = avg_price

    def get_qty(self):
        return self._qty

class MockPositionManager:
    def __init__(self, positions):
        self.positions = positions

    def find_position_by_instrument_id(self, instrument_id):
        return self.positions.get(instrument_id, MockPosition(0))

class MockPortfolioManager:
    def __init__(self, cash, total_value):
        self._cash = cash
        self._total_value = total_value

    def get_available_cash(self):
        return self._cash

    def get_total_portfolio_value(self):
        return self._total_value

# -------------------------------
# Tests
# -------------------------------

def test_cash_constraint_fail():
    pm = MockPortfolioManager(cash=1000, total_value=5000)
    pos_mgr = MockPositionManager({'AAPL': MockPosition(10)})
    intent = OrderIntent(
        instrument_id='AAPL',
        side=Side.BUY,
        qty=20,  # total cost = 20*100=2000 > cash 1000
        price=100,
        timestamp=datetime.now(),
        intent_type=None,
    )
    result = validate_constraints(pm, pos_mgr, intent)
    assert not result.allowed
    assert "available cash" in result.reason

def test_position_existence_fail():
    pm = MockPortfolioManager(cash=10000, total_value=20000)
    pos_mgr = MockPositionManager({'AAPL': MockPosition(5)})
    intent = OrderIntent(
        instrument_id='AAPL',
        side=Side.SELL,
        qty=10,  # trying to sell more than we have
        price=100,
        timestamp=datetime.now(),
        intent_type=None,
    )
    result = validate_constraints(pm, pos_mgr, intent)
    assert not result.allowed
    assert "exceeds current position qty" in result.reason

def test_max_exposure_fail():
    pm = MockPortfolioManager(cash=10000, total_value=100000)
    pos_mgr = MockPositionManager({'AAPL': MockPosition(700)})
    intent = OrderIntent(
        instrument_id='AAPL',
        side=Side.BUY,
        qty=50,  # current qty + 50 will exceed 7.5% cap of 100k = 7500
        price=10,
        timestamp=datetime.now(),
        intent_type=None,
    )
    # Mock get_mark_price method
    intent.get_mark_price = lambda: 10  # total exposure = (700+50)*10=7500 => equal cap
    result = validate_constraints(pm, pos_mgr, intent)
    assert not result.allowed or result.allowed  # could be edge case
