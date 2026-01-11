# The total exposure of an instrument cannot exceed 7.5%
PER_INSTRUMENT_EXPOSURE_CAP_PERCENTAGE = 0.075

class ConstraintResult:
    instrument_id: str
    allowed: bool
    reason: str


    def __init__(self, instrument_id: str, allowed: bool, reason: str = ""):
        self.instrument_id = instrument_id
        self.allowed = allowed
        self.reason = reason

    def is_allowed(self) -> bool:
        return self.allowed


