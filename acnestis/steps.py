import logging
import os
import tempfile
import shutil

from typing import Callable, Optional, Union, Dict, Any, NewType

from .command import process as command_process

logger = logging.getLogger(__name__)

CallableReturn = Callable[[str, str], None]


def using_folder(folder: str) -> CallableReturn:
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


def copy(from_folder: str, to_folder: str) -> CallableReturn:
    def _(source_root: str, target: str) -> None:
        shutil.copytree(
            os.path.join(source_root, from_folder),
            os.path.join(target, to_folder),
            dirs_exist_ok=True,
        )

    return _


def rm(folder: str) -> CallableReturn:
    def _(source_root: str, target: str) -> None:
        source: str = os.path.join(target, folder)
        shutil.rmtree(source, ignore_errors=True)

    return _


def git(url: str, branch: str = "master", subfolder: str = "") -> CallableReturn:
    from git import Repo

    from .command import process as command_process

    def _(source_root: str, target: str) -> None:
        with tempfile.TemporaryDirectory() as tmpdirname, tempfile.TemporaryDirectory() as tmpclone:
            repo = Repo.clone_from(url, tmpclone)
            repo.git.checkout(branch)
            shutil.rmtree(os.path.join(tmpclone, ".git"), ignore_errors=True)
            shutil.copytree(
                os.path.join(tmpclone, *subfolder.split("/")),
                tmpdirname,
                dirs_exist_ok=True,
            )

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


NestedDict = NewType("NestedDict", Dict[str, Union[str, Any]])


def folder_to_dict(folder_path: str, clean: bool = False) -> NestedDict:
    result: NestedDict = {}  # type: ignore[assignment]
    for item in sorted(os.listdir(folder_path)):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            with open(item_path, "r") as file:
                value: Any = file.read()
            if clean:
                os.remove(item_path)

            key, fext = os.path.splitext(item)
            if fext == ".json":
                import json

                value = json.loads(value)
            elif fext == ".yaml":
                import yaml  # type: ignore[import]

                value = yaml.load(value, Loader=yaml.FullLoader)
            elif fext == ".int":
                value = int(value)
            result[key] = value

        elif os.path.isdir(item_path):
            value = folder_to_dict(item_path, clean=clean)
            if clean:
                os.rmdir(item_path)
            key = item

            array_suffix = ".array"
            if key.endswith(array_suffix):
                key = key[: -len(array_suffix)]
                value = list(value.values())

            result[key] = value
    return result


def aggregate(into_file: str) -> CallableReturn:
    def _(source_root: str, target: str) -> None:
        with tempfile.TemporaryDirectory() as tmpdirname:
            command_process(target, tmpdirname, exist_ok=True)
            fdict = folder_to_dict(tmpdirname, clean=True)

        shutil.rmtree(target, ignore_errors=True)
        os.makedirs(target, exist_ok=True)

        with open(os.path.join(target, into_file), "w") as fh:
            if into_file.endswith(".json"):
                import json

                json.dump(fdict, fh)
            elif into_file.endswith(".yaml"):
                import yaml  # type: ignore[import]

                yaml.dump(fdict, fh)

    return _
