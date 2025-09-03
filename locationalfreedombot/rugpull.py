import logging
from typing import Dict


class RugPullChecker:
    """Checks token metadata for simple rug pull indicators."""

    def __init__(self, min_liquidity: float = 0.0) -> None:
        self.min_liquidity = min_liquidity
        self.logger = logging.getLogger(__name__)

    def is_safe(self, token: Dict) -> bool:
        liquidity = token.get("liquidity", 0.0)
        safe = liquidity >= self.min_liquidity
        if not safe:
            self.logger.warning(
                "Token %s failed rug pull check: liquidity %s below %s",
                token.get("symbol"),
                liquidity,
                self.min_liquidity,
            )
        return safe
