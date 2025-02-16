import logging
import os
import sys
from typing import Any, ClassVar

dt_fmt = "%Y-%m-%d %H:%M:%S"


def stream_supports_color(stream: Any) -> bool:
    is_a_tty = hasattr(stream, "isatty") and stream.isatty()

    if sys.platform != "win32":
        return is_a_tty

    # ANSICON checks for things like ConEmu
    # WT_SESSION checks if this is Windows Terminal
    # VSCode built-in terminal supports colour too
    return is_a_tty and (
        "ANSICON" in os.environ or "WT_SESSION" in os.environ or os.environ.get("TERM_PROGRAM") == "vscode"
    )


class _ColorFormatter(logging.Formatter):
    # ANSI codes are a bit weird to decipher if you're unfamiliar with them, so here's a refresher
    # It starts off with a format like \x1b[XXXm where XXX is a semicolon separated list of commands
    # The important ones here relate to colour.
    # 30-37 are black, red, green, yellow, blue, magenta, cyan and white in that order
    # 40-47 are the same except for the background
    # 90-97 are the same but "bright" foreground
    # 100-107 are the same as the bright ones but for the background.
    # 1 means bold, 2 means dim, 0 means reset, and 4 means underline.

    LEVEL_COLOURS: ClassVar = [
        (logging.DEBUG, "\x1b[40;1m"),
        (logging.INFO, "\x1b[34;1m"),
        (logging.WARNING, "\x1b[33;1m"),
        (logging.ERROR, "\x1b[31m"),
        (logging.CRITICAL, "\x1b[41m"),
    ]

    FORMATS: ClassVar = {
        level: logging.Formatter(
            f"\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m[{{category}}]\x1b[0m \x1b[35m%(name)s\x1b[0m %(message)s",
            dt_fmt,
        )
        for level, colour in LEVEL_COLOURS
    }

    def format(self, record: logging.LogRecord) -> str:
        if record.name.startswith("wirecraft.server"):
            record.name = record.name[17:]
            category = "SERVER"
        elif record.name.startswith("wirecraft.client"):
            record.name = record.name[17:]
            category = "CLIENT"
        else:
            category = "OTHER "

        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        # Override the traceback to always print in red
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f"\x1b[31m{text}\x1b[0m"

        output = formatter.format(record)
        output = output.format(category=category)

        # Remove the cache layer
        record.exc_text = None
        return output


def init_logger(level: int = logging.INFO) -> None:
    """
    Initialize the logger with the given level.

    :param level: The logging level to use.
    """
    handler = logging.StreamHandler()
    if stream_supports_color(handler.stream):
        handler.setFormatter(_ColorFormatter())
    else:
        handler.setFormatter(logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"))
    logging.basicConfig(
        handlers=[handler],
        level=level,
    )

    logging.getLogger().setLevel(level)
