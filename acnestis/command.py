import os
import shutil
import logging
import tempfile
from typing import Dict, Any

logger = logging.getLogger(__name__)

# maybe we should have a global variable that highlight a global call of process?


def process(source: str, target: str, exist_ok: bool = False) -> None:
    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(source, target, dirs_exist_ok=exist_ok)
    for root, _, files in os.walk(target):
        for file in files:
            if file == ".acnestis.py":
                logger.debug("Processing {} in {}".format(file, root))

                abs_file = os.path.join(root, file)
                with open(abs_file, "r") as f:
                    globals: Dict[str, Any] = {}
                    exec(f.read(), globals)
                    processor = globals["PROCESSOR"]
                    processor.process(
                        os.path.abspath(os.path.join(source, root)),
                        os.path.abspath(os.path.join(target, root)),
                    )
                os.unlink(abs_file)

                if processor.replace_folder_with_file:
                    with tempfile.TemporaryDirectory() as tmpdirname:
                        shutil.move(
                            os.path.join(root, processor.replace_folder_with_file),
                            tmpdirname,
                        )
                        shutil.rmtree(root)
                        shutil.copy(
                            os.path.join(
                                tmpdirname, processor.replace_folder_with_file
                            ),
                            root,
                        )


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
