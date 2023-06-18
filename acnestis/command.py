import os
import shutil
import logging
import tempfile
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# maybe we should have a global variable that highlight a global call of process?


def process(source: str, target: str, exist_ok: bool = False) -> None:
    def get_globals_from_py(code: str, abs_file: str) -> Dict[str, Any]:
        globals: Dict[str, Any] = {"__file__": abs_file}
        exec(code, globals)
        return globals

    def get_process_from_py(code: str, abs_file: str) -> Any:
        return get_globals_from_py(code, abs_file)["PROCESSOR"]

    def get_process_from_yaml(
        code: str, py_globals: Optional[Dict[str, Any]] = None
    ) -> Any:
        from .yaml import main

        return main(code, py_globals=py_globals)

    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(source, target, dirs_exist_ok=exist_ok)
    for root, _, files in os.walk(target):
        if ".acnestis.yaml" in files:
            file = ".acnestis.yaml"
        elif ".acnestis.py" in files:
            file = ".acnestis.py"
        else:
            continue

        logger.debug("Processing {} in {}".format(file, root))

        rel_root = os.path.relpath(root, target)
        abs_file = os.path.join(root, file)
        abs_source_file = os.path.abspath(os.path.join(source, rel_root, file))
        with open(abs_file, "r") as f:
            if file.endswith(".yaml"):
                py_globals = None
                if ".acnestis.py" in files:
                    abs_py_file = os.path.join(root, ".acnestis.py")
                    with open(abs_py_file, "r") as py_f:
                        py_globals = get_globals_from_py(py_f.read(), abs_source_file)
                    os.unlink(abs_py_file)
                processor = get_process_from_yaml(f.read(), py_globals=py_globals)

            elif file.endswith(".py"):
                processor = get_process_from_py(f.read(), abs_source_file)

        os.unlink(abs_file)
        processor.process(
            os.path.abspath(os.path.join(source, rel_root)),
            os.path.abspath(os.path.join(target, rel_root)),
        )

        if processor.as_file:
            with tempfile.TemporaryDirectory() as tmpdirname:
                shutil.move(
                    os.path.join(root, processor.as_file),
                    tmpdirname,
                )
                shutil.rmtree(root)
                shutil.copy(
                    os.path.join(tmpdirname, processor.as_file),
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

    if hasattr(args, "func"):
        args.func(args)
