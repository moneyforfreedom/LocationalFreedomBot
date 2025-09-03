import argparse
import json
import logging
from pathlib import Path

from locationalfreedombot.bot import TradingBot

CONFIG_PATH = Path("config/config.yaml")


def load_config(path: Path = CONFIG_PATH):
    with open(path) as f:
        return json.load(f)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="LocationalFreedomBot controller")
    parser.add_argument("command", choices=["start", "stop", "status"])
    args = parser.parse_args()

    config = load_config()
    bot = TradingBot(config)

    if args.command == "start":
        bot.start()
    elif args.command == "stop":
        bot.stop()
    elif args.command == "status":
        print(bot.status())


if __name__ == "__main__":
    main()
