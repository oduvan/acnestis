import os
import shutil
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def process(source: str, target: str, exist_ok: bool = False) -> None:
    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(source, target, dirs_exist_ok=exist_ok)
    for root, _, files in os.walk(target):
        for file in files:
            if file == ".acnestis.py":
                logger.debug("Processing {} in {}".format(file, root))
                os.chdir(root)
                with open(file, "r") as f:
                    globals: Dict[str, Any] = {}
                    exec(f.read(), globals)
                    globals["PROCESSOR"].process(".")
                os.unlink(file)


def console() -> None:
    import argparse

    LEVELS: list[int] = [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    ]

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", dest="verbose", default=3, type=int, help="verbose level")

    subparsers = parser.add_subparsers(help="sub-command help")

    parser_process = subparsers.add_parser(
        "process", help="convert acnestis folder to target folder"
    )
    parser_process.add_argument("source")
    parser_process.add_argument("target")
    parser_process.add_argument("--exist-ok", action="store_true")

    def sub_process(args: argparse.Namespace) -> None:
        process(args.source, args.target, exist_ok=args.exist_ok)

    parser_process.set_defaults(func=sub_process)
    args = parser.parse_args()
    logging.basicConfig(level=LEVELS[args.verbose])

    args.func(args)
