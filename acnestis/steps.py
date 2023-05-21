import logging

from typing import Callable

logger = logging.getLogger(__name__)


def copy_folder(source: str) -> Callable[[str], None]:
    import tempfile
    import shutil

    def _(target: str) -> None:
        with tempfile.TemporaryDirectory() as tmpdirname:
            logging.debug("Copying {} to {}".format(source, tmpdirname))
            shutil.copytree(source, tmpdirname, dirs_exist_ok=True)

            logging.debug("Copying {} to {}".format(target, tmpdirname))
            shutil.copytree(target, tmpdirname, dirs_exist_ok=True)

            logging.debug("Copying {} to {}".format(tmpdirname, target))
            shutil.copytree(tmpdirname, target, dirs_exist_ok=True)

    return _
