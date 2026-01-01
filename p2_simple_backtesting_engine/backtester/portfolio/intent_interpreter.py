from backtester.strategy.signal import Signal
from backtester.strategy.portfolio.order_intent import OrderIntent, Intent
from backtester.strategy.side import Side


# This is kind of like factory class but essentially it is an API that hides how we translate signals into orderIntents
# To be fair this might be a tad over-engineered but better to keep things modular and separate so that we can extend things easily later

class IntentInterpreter:

    def interpret_signals(self, signals: list[Signal]) -> list[OrderIntent]:
        # take the data and take the signal (maybe just keep it in the same dataframe)
        # then generate an OrderIntent out of it, refer to order_intent to see what is in there
        orderIntents = []

        for signal in signals:
            orderIntents.append(
                OrderIntent(
                    instrument_id=signal.instrument_id, 
                    side=signal.side, 
                    qty=signal.qty, 
                    intent_type=self.get_intent_type(signal)
                )
        )

        return orderIntents

    def get_intent_type(self, signal: Signal) -> Intent:
        if signal.side == Side.BUY:
            return Intent.ENTRY
        elif signal.side == Side.SELL:
            return Intent.EXIT
