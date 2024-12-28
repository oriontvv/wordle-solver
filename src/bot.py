from __future__ import annotations

from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import os
from time import time
from expiring_dict import ExpiringDict
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import typing


from words_loader import load_words
from solver import Solver

cur_dir = Path(__file__).parent
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)
logger = logging.getLogger(__name__)

file_handler = RotatingFileHandler(cur_dir.parent / "history.log", maxBytes=10**6, backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(file_handler)

sessions: ExpiredSessionsStorage
HELP = """Wordle solver:
/new ru : start new game with russian dict
/new en : start new game with english dict

FORMAT: characters must be delimeted with space:
a i- e t+ r+
x       : character solved
x+      : character is in the word
x-      : character is NOT in the word
"""


class RefreshExpiringDict(ExpiringDict):
    def refresh_tll(self, key: str) -> None:
        with self._ExpiringDict__lock:
            for ts, _key in self._ExpiringDict__keys:
                if key == _key:
                    self._ExpiringDict__keys.discard((ts, key))
                    break
            self._ExpiringDict__keys.add((time() + self._ExpiringDict__ttl, key))


class ExpiredSessionsStorage:
    def __init__(
        self,
        lang: str,
        length: int,
        expire_session_ttl: int,
        expire_session_interval: int,
    ):
        self.lang = lang
        self.length = length
        self.sessions = RefreshExpiringDict(ttl=expire_session_ttl, interval=expire_session_interval)

    def __getitem__(self, key: str) -> Session:
        try:
            session = self.sessions[key]
            self.sessions.refresh_tll(key)
            return session
        except KeyError:
            session = Session(self.lang, self.length)
            self.sessions[key] = session
            return session


class Session:
    def __init__(self, lang: str, length: int):
        self.lang = lang
        self.length = length
        words = load_words(lang, length)
        self.solver = Solver(words, length)

    async def send_variants(self, update: Update) -> bool:
        if self.solver.is_done():
            text = "Is game completed? type `new <lang>` for new game"
            await send_text(text, update)
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
        await send_text(output, update)
        return True

    async def process_input(self, text: str, update: Update):
        try:
            self.solver.add_guess_result(text)
            await self.send_variants(update)
        except Exception as e:
            await send_error(e, update)

    async def reset(self, lang: str | None, update: Update):
        words = load_words(lang or self.lang, self.length)
        self.solver.reset(words)
        try:
            await self.send_variants(update)
        except Exception as e:
            await send_error(e, update)


@typing.no_type_check
async def guess_word_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    in_msg = update.message.text
    user = update.effective_user.username
    logger.info(f"{user} sent '{in_msg}'")
    session = sessions[user]
    try:
        await session.process_input(in_msg, update)
    except Exception as e:
        await send_error(e, update)


async def send_error(e: Exception, update: Update) -> None:
    text = f"Error {e}"
    logger.info(text)
    await send_text(text, update)
    await send_help(update)


async def send_help(update: Update) -> None:
    await send_text(HELP, update)


@typing.no_type_check
async def send_text(text: str, update: Update) -> None:
    await update.message.reply_text(text[:512])


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_help(update)


@typing.no_type_check
async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    load_dotenv()
    tg_token = os.getenv("TELEGRAM_TOKEN")
    expire_session_ttl = int(os.getenv("EXPIRE_SESSION_TTL", 4 * 60 * 60))
    expire_session_interval = int(os.getenv("EXPIRE_SESSION_INTERVAL", 10 * 60))

    global sessions
    sessions = ExpiredSessionsStorage(lang, length, expire_session_ttl, expire_session_interval)

    assert tg_token, "TELEGRAM_TOKEN env var not found"

    application = Application.builder().token(tg_token).build()
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("new", new_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guess_word_command))

    logger.info("started")
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
