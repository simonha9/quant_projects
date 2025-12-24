import pandas as pd

# This is the meat of the portfolio manager, it should manage the actual flow detailed in the readme.

class PortfolioManager:
    data: pd.DataFrame

    def __init__(self, data: pd.DataFrame):
        self.data = data

    