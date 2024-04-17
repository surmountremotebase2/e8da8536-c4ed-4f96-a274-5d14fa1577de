from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker symbol for the asset you wish to trade
        self.ticker = "AAPL"
    
    @property
    def interval(self):
        # Set the trading interval to daily
        return "1day"
    
    @property
    def assets(self):
        # List of ticker symbols to be included in the strategy
        return [self.ticker]
    
    @property
    def data(self):
        # No additional data needed beyond default OHLCV
        return []

    def run(self, data):
        # Initialize allocation to none
        allocation = 0.0
        # Get the latest data for calculations
        d = data["ohlcv"]
        
        if len(d) > 26:  # Ensure there's enough data for calculation
            # Calculate technical indicators for AAPL
            rsi = RSI(self.ticker, d, 14)
            ema_short = EMA(self.ticker, d, 12)
            ema_long = EMA(self.ticker, d, 26)
            macd = MACD(self.ticker, d, 12, 26)['MACD'][-1] # Extracting the last value of the MACD list

            # Decision logic
            if rsi[-1] < 30 and ema_short[-1] > ema_long[-1] and macd > 0:
                # Conditions met for an uptrend, allocate 100%
                allocation = 1.0
            elif rsi[-1] > 70 or ema_short[-1] < ema_long[-1]:
                # Conditions indicate a downtrend or correction, reduce exposure
                allocation = 0.0
            else:
                # Neutral conditions, maintain existing allocation
                # Can adjust to previous allocation or other logic
                allocation = 0.5

        # Return the TargetAllocation object with the decided allocation
        return TargetAllocation({self.ticker: allocation})