

# This is kind of like factory class but essentially it is an API that hides how we translate signals into orderIntents
# To be fair this might be a tad over-engineered but better to keep things modular and separate so that we can extend things easily later

class IntentInterpreter:

    def interpretSignals(data: pd.DataFrame, signals: pd.DataFrame) -> OrderIntent[]:
        # take the data and take the signal (maybe just keep it in the same dataframe)
        # then generate an OrderIntent out of it, refer to order_intent to see what is in there

        