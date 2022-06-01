from argparse import ArgumentParser

from app import App


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--lang", help="language", default="ru")
    parser.add_argument("--length", help="length of words", default=5)
    return parser.parse_args()


def main():
    args = parse_args()
    app = App(lang=args.lang, length=args.length)
    app.run()


if __name__ == "__main__":
    main()
