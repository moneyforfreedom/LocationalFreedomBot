import logging
from typing import Dict

from .wallet import Wallet
from .strategy import RSIStrategy
from .rugpull import RugPullChecker
from .execution import TradeExecutor


class TradingBot:
    """High level trading bot orchestrating modules."""

    def __init__(self, config: Dict) -> None:
        self.config = config
        wallet_cfg = config.get("wallet", {})
        strategy_cfg = config.get("strategy", {})
        rug_cfg = config.get("rugpull", {})
        self.wallet = Wallet(wallet_cfg.get("balance", 0.0))
        self.strategy = RSIStrategy(
            period=strategy_cfg.get("rsi_period", 14),
            overbought=strategy_cfg.get("overbought", 70),
            oversold=strategy_cfg.get("oversold", 30),
        )
        self.checker = RugPullChecker(rug_cfg.get("min_liquidity", 0.0))
        self.executor = TradeExecutor(self.wallet, self.checker)
        self.running = False
        self.logger = logging.getLogger(__name__)

    def start(self) -> None:
        self.running = True
        trade_cfg = self.config.get("trade", {})
        token_cfg = self.config.get("token", {})
        prices = trade_cfg.get("price_history", [])
        amount = trade_cfg.get("amount", 0.0)
        signal = self.strategy.generate_signal(prices)
        self.logger.info("Strategy signal: %s", signal)
        self.executor.execute(signal, token_cfg, amount)

    def stop(self) -> None:
        self.running = False
        self.logger.info("Bot stopped")

    def status(self) -> str:
        return "running" if self.running else "stopped"
