import datetime

from backtester.portfolio.ledger import LedgerRecord
from backtester.strategy.side import Side

# The RoundTripTrade object is a reconstruction of the filled trades from the ledger
# It denotes an entry fill that opens risk, and a exit fill that closes the risk
# Some time interval
# A realized PNL

class RoundTripTrade:
    def __init__(
        self,
        instrument_id: str,
        entry_time: datetime,
        exit_time: datetime,
        entry_price: float,
        exit_price: float,
        qty: int,
        realized_pnl: float,
        fills: list[int],
        is_partial: bool,
    ):
        self.instrument_id = instrument_id
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.holding_period = exit_time - entry_time

        self.qty = qty                    # signed (+ long, - short)
        self.entry_price = entry_price    # VWAP of entry fills
        self.exit_price = exit_price      # VWAP of exit fills

        self.realized_pnl = realized_pnl
        self.return_pct = (
            realized_pnl / (abs(qty) * entry_price)
            if qty != 0 and entry_price != 0
            else 0.0
        )

        self.fills = fills                # ledger record ids
        self.is_partial = is_partial      # closed via reversal or forced close

    

def reconstruct_trades(records: list[LedgerRecord]):
    trades = []
    # Sort it chronologically so we don't have to do it later
    records.sort(key=lambda x : x.timestamp)

    # dict(string, list[LedgerRecord])
    records_grouped_by_instrument_id_chronological = {}

    for record in records:
        if (records_grouped_by_instrument_id_chronological[record.instrument_id]):
            records_grouped_by_instrument_id_chronological[record.instrument_id].append(record)
        else:
            records_grouped_by_instrument_id_chronological[record.instrument_id] = []

    for instrument_id, instrument_records in records_grouped_by_instrument_id_chronological.items():
        instrument_trades = []
        i = 0
        n = len(instrument_records)

        # Track open trade state
        current_qty = 0           # signed: + long, - short
        entry_qty = 0
        entry_value = 0.0
        entry_time = None
        fills = []

        while i < n:
            r = instrument_records[i]
            qty_delta = r.qty if r.side == Side.BUY else -r.qty
            prev_qty = current_qty
            current_qty += qty_delta

            # Open a new trade if none exists
            if prev_qty == 0 and current_qty != 0:
                entry_time = r.timestamp
                entry_qty = abs(qty_delta)
                entry_value = r.qty * r.price
                fills = [r.id]  # start collecting ledger record ids
            elif prev_qty != 0:
                # Accumulate open trade
                entry_qty += abs(qty_delta)
                entry_value += r.qty * r.price
                fills.append(r.id)

            # Check for zero-cross (trade close)
            if prev_qty != 0 and current_qty == 0:
                exit_time = r.timestamp
                exit_value = 0.0
                for fill_id in fills:
                    # Lookup record to compute exit VWAP (simplest way: use r.price here or sum over exit fills)
                    exit_value += next(x.price * x.qty for x in instrument_records if x.id == fill_id)
                # Compute VWAPs
                entry_vwap = entry_value / entry_qty
                exit_vwap = exit_value / entry_qty
                realized_pnl = (exit_vwap - entry_vwap) * entry_qty * (1 if prev_qty > 0 else -1)

                # Construct the round-trip trade
                trade = RoundTripTrade(
                    instrument_id=r.instrument_id,
                    entry_time=entry_time,
                    exit_time=exit_time,
                    entry_price=entry_vwap,
                    exit_price=exit_vwap,
                    qty=entry_qty * (1 if prev_qty > 0 else -1),
                    realized_pnl=realized_pnl,
                    fills=fills.copy(),
                    is_partial=False  # fully closed
                )
                instrument_trades.append(trade)

                # Reset for next trade
                current_qty = 0
                entry_qty = 0
                entry_value = 0.0
                entry_time = None
                fills = []

            # Handle zero-cross reversal (optional: open opposite trade immediately)
            elif prev_qty != 0 and (current_qty * prev_qty < 0):
                # Trade closed and new position opened
                exit_time = r.t_



        return trades
        
