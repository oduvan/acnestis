import logging
import os

from typing import Callable, Optional, TypeVar

logger = logging.getLogger(__name__)

CallableReturn = Callable[[str, str], None]


def copy_folder(folder: str) -> CallableReturn:
    import tempfile
    import shutil
    from .command import process as command_process

    def _(source_root: str, target: str) -> None:
        source: str = (
            folder if os.path.isabs(folder) else os.path.join(source_root, folder)
        )
        with tempfile.TemporaryDirectory() as tmpdirname:
            logging.debug("Copying {} to {}".format(source, tmpdirname))
            shutil.copytree(source, tmpdirname, dirs_exist_ok=True)

            logging.debug("Copying {} to {}".format(target, tmpdirname))
            shutil.copytree(target, tmpdirname, dirs_exist_ok=True)

            logging.debug("Copying {} to {}".format(tmpdirname, target))
            command_process(tmpdirname, target, exist_ok=True)

    return _


def concat_files(into_file: str, after_file: Optional[str] = "\n") -> CallableReturn:
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


def code(code: str) -> CallableReturn:
    def _(source_root: str, target: str) -> None:
        exec(code, {"source_root": source_root, "target": target})

    return _


def docker(image: str, skip_pull: bool = False) -> CallableReturn:
    def _(source_root: str, target: str) -> None:
        import docker as docker_module

        client = docker_module.from_env()

        if not skip_pull:
            client.images.pull(image)

        volumes = {
            source_root: {"bind": "/data_input", "mode": "rw"},
            target: {"bind": "/data_output", "mode": "rw"},
        }

        container = client.containers.run(image, detach=True, volumes=volumes)
        container.wait()
        container.remove()

    return _
