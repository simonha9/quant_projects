# This is a super basic SMA crossover implementation
# We will use the common 50,200 and look for intersections

class SMACrossover(Strategy):
    def execute(self, data: pd.DataFrame):
        # get the 50 SMA
        data['SMA_50'] = data['close'].rolling(window=50).mean()
        # get the 200 SMA
        data['SMA_200'] = data['close'].rolling(window=200).mean()

        # When do they intersect?
        # They intersect when :
        # SMA_50 was below SMA_200 and now is going above
        #   in this case, we should buy
        # SMA_50 was above SMA_200 and now is going below
        #   in this case, we should sell

        # We definitely want to cache this
        prev_sma_50 = data['SMA_50'].shift(1)
        prev_sma_200 = data['SMA_200'].shift(1)


        data['signal'] = 0
        data.loc[[(prev_sma_50 <= prev_sma_200) & (data['SMA_50'] > data['SMA_200'])], 'signal'] = 1  # Buy
        data.loc[[(prev_sma_50 > prev_sma_200) & (data['SMA_50'] < data['SMA_200'])], 'signal'] = -1  # Sell

        return data


