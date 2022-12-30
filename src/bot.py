from __future__ import annotations

from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import os
from collections import defaultdict

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

from words import load_words
from solver import Solver

cur_dir = Path(__file__).parent
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)
logger = logging.getLogger(__name__)

file_handler = RotatingFileHandler(
    cur_dir / "history.log", maxBytes=10**6, backupCount=5
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(file_handler)

sessions: dict[str, "Session"]
HELP = """Wordle solver:
/new <lang> \t\t start new game

x  \t\t\t character solved
x+ \t\t\t character is in the word
x- \t\t\t character is NOT in the word
characters should be delimeted with space:
a i- e t+ r+"""


class Session:
    def __init__(self, lang: str, length: int):
        self.lang = lang
        self.length = length
        words = load_words(lang, length)
        self.solver = Solver(words, length)

    def send_variants(self, update: Update) -> bool:
        if self.solver.is_done():
            update.message.reply_text(
                "game is completed? select new <lang> for new game"
            )
            return False
        output = ""
        variants = self.solver.get_next_guess()
        if variants:
            output += "\n".join(variants) + "\n\n"
            guess = variants[0]
            if guess is None:
                output += "I don't know such a word..\n"
            else:
                output += f"Try '{guess}'\n"

        output += f"Total variants: {self.solver.total_variants()}"
        update.message.reply_text(output)
        return True

    def process_input(self, text: str, update: Update):
        try:
            self.solver.add_guess_result(text)
            self.send_variants(update)
        except Exception as e:
            update.message.reply_text(f"Error: {e}")

    def reset(self, lang: str | None, update: Update):
        words = load_words(lang or self.lang, self.length)
        self.solver.reset(words)
        try:
            self.send_variants(update)
        except Exception as e:
            update.message.reply_text(f"Error: {e}")


def guess_word_command(update: Update, context: CallbackContext) -> None:
    in_msg = update.message.text
    user = update.effective_user.username
    logger.info(f"{user} sent '{in_msg}'")
    session = sessions[user]
    try:
        session.process_input(in_msg, update)
    except Exception as e:
        msg = f"Error {e}\n{HELP}"
        logger.info(msg)
        update.message.reply_text(msg[:512])


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(HELP)


def new_command(update: Update, context: CallbackContext) -> None:
    cmd = update.message.text
    try:
        _, lang = cmd.split()
    except ValueError:
        lang = None

    user = update.effective_user.username
    logger.info(f"{user} started new game '{lang}'")
    session = sessions[user]
    session.reset(lang=lang, update=update)


def run_bot(lang: str, length: int):
    global sessions
    sessions = defaultdict(lambda: Session(lang=lang, length=length))

    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    assert token, "token not found"
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("new", new_command))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, guess_word_command)
    )

    updater.start_polling()
    logger.info("started")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
