import logging
from typing import List


class RSIStrategy:
    """Very small RSI based trading strategy."""

    def __init__(self, period: int = 14, overbought: float = 70, oversold: float = 30) -> None:
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
        self.logger = logging.getLogger(__name__)

    def compute_rsi(self, prices: List[float]) -> float:
        if len(prices) <= self.period:
            raise ValueError("Not enough price data to compute RSI")
        gains = 0.0
        losses = 0.0
        # Use the last `period` differences
        for i in range(len(prices) - self.period, len(prices)):
            delta = prices[i] - prices[i - 1]
            if delta > 0:
                gains += delta
            else:
                losses -= delta
        avg_gain = gains / self.period
        avg_loss = losses / self.period
        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        self.logger.debug("RSI value computed: %s", rsi)
        return rsi

    def generate_signal(self, prices: List[float]) -> str:
        rsi = self.compute_rsi(prices)
        if rsi < self.oversold:
            return "buy"
        if rsi > self.overbought:
            return "sell"
        return "hold"
