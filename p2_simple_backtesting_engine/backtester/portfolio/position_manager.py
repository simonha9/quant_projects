from datetime import datetime

# Note that this is 1:1 to instruments, so we should be able to index by instrument_ids
class Position:
    instrument_id: str
    qty: int
    avg_entry_price: float
    open_timestamp: datetime
    realized_pnl: float

    def __init__(self, instrument_id: str, qty: int, avg_entry_price: float, open_timestamp: datetime, realized_pnl: float):
        self.instrument_id = instrument_id
        self.qty = qty
        self.avg_entry_price = avg_entry_price
        self.open_timestamp = open_timestamp
        self.realized_pnl = realized_pnl

    def get_qty(self) -> int:
        return self.qty
    
    def get_avg_entry_price(self) -> float:
        return self.avg_entry_price
    
    def recalculate_avg_entry_price(self, qty_delta: int, price: float) -> float:
        # get total value + price*qty_delta / total qty + qty_delta

        total_value = self.qty * self.avg_entry_price
        value_delta = qty_delta * price
        resulting_qty = self + qty_delta

        self.avg_entry_price = (total_value + value_delta) / resulting_qty
        return self.avg_entry_price
    
    def get_exposure(self, mark_price: float) -> float:
        return self.qty * mark_price
    
    

class PositionManager:

    def __init__(self):
        self.positions = []
    
    def add_position(self, position: Position) -> None:
        self.positions.append(position)
    
    def get_positions(self) -> list[Position]:
        return self.positions
    
    def find_position_by_instrument_id(self, instrument_id: str) -> Position:
        return self.positions.find(lambda x: x.instrument_id == instrument_id)
    
    def get_total_position_equity(self) -> float:
        total_equity = 0.0
        for position in self.positions:
            total_equity += position.get_value()
        return total_equity