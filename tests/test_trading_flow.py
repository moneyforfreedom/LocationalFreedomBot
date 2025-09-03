import json
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1]))

from locationalfreedombot.wallet import Wallet
from locationalfreedombot.strategy import RSIStrategy
from locationalfreedombot.rugpull import RugPullChecker
from locationalfreedombot.execution import TradeExecutor


CONFIG_PATH = Path("config/config.yaml")


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def test_trade_executes_when_safe():
    cfg = load_config()
    wallet = Wallet(cfg["wallet"]["balance"])
    strategy = RSIStrategy(
        cfg["strategy"]["rsi_period"],
        cfg["strategy"]["overbought"],
        cfg["strategy"]["oversold"],
    )
    checker = RugPullChecker(cfg["rugpull"]["min_liquidity"])
    executor = TradeExecutor(wallet, checker)

    prices = cfg["trade"]["price_history"]
    signal = strategy.generate_signal(prices)
    token = cfg["token"]
    amount = cfg["trade"]["amount"]

    assert executor.execute(signal, token, amount)
    assert wallet.get_balance() == cfg["wallet"]["balance"] - amount


def test_trade_blocked_on_rugpull():
    wallet = Wallet(1000)
    checker = RugPullChecker(min_liquidity=50000)
    executor = TradeExecutor(wallet, checker)

    token = {"symbol": "SCAM", "liquidity": 10}
    signal = "buy"
    amount = 100

    assert not executor.execute(signal, token, amount)
    assert wallet.get_balance() == 1000
