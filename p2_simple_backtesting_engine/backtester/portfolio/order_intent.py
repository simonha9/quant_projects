import datetime
import uuid
from enum import Enum


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
    ENTRY = 1
    EXIT = 2
    REBALANCE = 3
    RISK_REDUCTION = 4
    STOP = 5

class OrderIntent:
    order_intent_id: uuid
    instrument_id: str
    side: Side
    qty: int
    timestamp: datetime
    intent_type: Intent

    