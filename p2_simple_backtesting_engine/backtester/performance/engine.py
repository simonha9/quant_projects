
from backtester.portfolio.ledger import Ledger

class PerformanceEngine:
    def __init__(self, ledger: Ledger, price_provider, initial_cash: float):
        self.ledger = ledger
        self.price_provider = price_provider
        self.initial_cash = initial_cash

        self.positions: dict[str, Position] = {}
        self.cash = initial_cash
        self.snapshots: list[PortfolioSnapshot] = []
