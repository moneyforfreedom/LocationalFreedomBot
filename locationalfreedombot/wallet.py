import logging


class Wallet:
    """Simple wallet to manage balances."""

    def __init__(self, balance: float = 0.0) -> None:
        self.balance = float(balance)
        self.logger = logging.getLogger(__name__)

    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.logger.info("Deposited %s", amount)

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.logger.info("Withdrew %s", amount)

    def get_balance(self) -> float:
        return self.balance
