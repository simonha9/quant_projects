class Strategy():
    @abstractmethod
    def execute(self, data: pd.DataFrame):
        """
        Executes the strategy that is currently set but must be 
        implemeneted in the subclass.  The client passes what strategy
        they want to use.
        """
        pass