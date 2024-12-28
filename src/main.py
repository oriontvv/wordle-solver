from __future__ import annotations

from argparse import ArgumentParser

from cli_app import CliApp
from bot import run_bot


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--lang", help="language", default="ru")
    parser.add_argument("--length", help="length of words", default=5)
    parser.add_argument("--bot", help="run telegram bot", default=False, action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.bot:
        run_bot(lang=args.lang, length=args.length)
    else:
        app = CliApp(lang=args.lang, length=args.length)
        app.run()


if __name__ == "__main__":
    main()
