import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1]))

from locationalfreedombot.rugpull import RugPullChecker


def test_rugpull_checker_flags_low_liquidity():
    checker = RugPullChecker(min_liquidity=1000)
    assert not checker.is_safe({"symbol": "BAD", "liquidity": 10})
    assert checker.is_safe({"symbol": "GOOD", "liquidity": 5000})
