import logging
import os

from typing import Callable, Optional, NewType

logger = logging.getLogger(__name__)


def copy_folder(folder: str) -> Callable[[str, str], None]:
    import tempfile
    import shutil

    def _(source_root: str, target: str) -> None:
        source: str = os.path.join(source_root, folder)
        with tempfile.TemporaryDirectory() as tmpdirname:
            logging.debug("Copying {} to {}".format(source, tmpdirname))
            shutil.copytree(source, tmpdirname, dirs_exist_ok=True)

            logging.debug("Copying {} to {}".format(target, tmpdirname))
            shutil.copytree(target, tmpdirname, dirs_exist_ok=True)

            logging.debug("Copying {} to {}".format(tmpdirname, target))
            shutil.copytree(tmpdirname, target, dirs_exist_ok=True)

    return _


def concat_files(
    into_file: str, after_file: Optional[str] = "\n"
) -> Callable[[str, str], None]:
    def _(source_root: str, target: str) -> None:
        files = [
            name
            for name in os.listdir(target)
            if not name.startswith(".") and os.path.isfile(os.path.join(target, name))
        ]

        with open(os.path.join(target, into_file), "w") as fh:
            for file in sorted(files):
                with open(os.path.join(target, file), "r") as f:
                    fh.write(f.read())
                    if after_file:
                        fh.write(after_file)

    return _
