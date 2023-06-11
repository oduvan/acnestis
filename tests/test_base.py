import tempfile
import os
import shutil
import pytest

from acnestis.command import process

from .tools import folder_to_dict

params_removed_file_name = pytest.mark.parametrize(
    "removed_file_name", [".acnestis.yaml", ".acnestis.py"]
)


def process_dict(path, removed_file_name=None):
    with tempfile.TemporaryDirectory() as tempfolder:
        shutil.copytree(path, os.path.join(tempfolder, "source"))
        if removed_file_name:
            if isinstance(removed_file_name, str):
                os.unlink(os.path.join(tempfolder, "source", removed_file_name))
            else:
                for name in removed_file_name:
                    os.unlink(os.path.join(tempfolder, "source", name))
        process(
            os.path.join(tempfolder, "source"),
            os.path.join(tempfolder, "result"),
            exist_ok=True,
        )
        return folder_to_dict(os.path.join(tempfolder, "result"))


@params_removed_file_name
def test_source_simple_copy(removed_file_name):
    assert process_dict(
        "tests/data/001_source_simple_copy", os.path.join("rosi", removed_file_name)
    ) == folder_to_dict("tests/data/001_source_simple_copy_result")


@params_removed_file_name
def test_concat_poem(removed_file_name):
    assert process_dict(
        "tests/data/002_concat_poem", os.path.join("poem.txt", removed_file_name)
    ) == folder_to_dict("tests/data/002_concat_poem_result")


def test_concat_poem_overwrite():
    assert process_dict("tests/data/003_concat_poem_overwrite") == folder_to_dict(
        "tests/data/003_concat_poem_overwrite_result"
    )


@params_removed_file_name
def test_code(removed_file_name):
    assert process_dict("tests/data/005_code", removed_file_name) == folder_to_dict(
        "tests/data/005_code_result"
    )


@params_removed_file_name
def test_docker_svgo(removed_file_name):
    assert process_dict(
        "tests/data/006_docker_svgo", removed_file_name
    ) == folder_to_dict("tests/data/006_docker_svgo_result")


@params_removed_file_name
def test_git_clone(removed_file_name):
    assert process_dict("tests/data/007_git", removed_file_name) == folder_to_dict(
        "tests/data/007_git_result"
    )


def test_git_processing():
    assert process_dict("tests/data/008_git_processing") == folder_to_dict(
        "tests/data/008_git_processing_result"
    )


def test_git_subfolder():
    assert process_dict("tests/data/009_git_subfolder") == folder_to_dict(
        "tests/data/009_git_subfolder_result"
    )
