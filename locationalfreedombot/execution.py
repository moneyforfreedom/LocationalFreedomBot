import logging
from typing import Dict

from .wallet import Wallet
from .rugpull import RugPullChecker


class TradeExecutor:
    """Executes trades if they pass rug pull checks and funds are available."""

    def __init__(self, wallet: Wallet, checker: RugPullChecker) -> None:
        self.wallet = wallet
        self.checker = checker
        self.logger = logging.getLogger(__name__)

    def execute(self, signal: str, token: Dict, amount: float) -> bool:
        if signal != "buy":
            self.logger.info("No trade executed for signal %s", signal)
            return False
        if not self.checker.is_safe(token):
            self.logger.warning("Trade blocked for token %s", token.get("symbol"))
            return False
        try:
            self.wallet.withdraw(amount)
        except ValueError:
            self.logger.error("Insufficient funds for trade")
            return False
        self.logger.info("Executed trade for token %s amount %s", token.get("symbol"), amount)
        return True
