import tempfile
import os
import shutil
import pytest

from acnestis.command import process

from .tools import folder_to_dict

params_removed_file_name = pytest.mark.parametrize(
    "removed_file_name", [".acnestis.yaml", ".acnestis.py"]
)


@params_removed_file_name
def test_source_simple_copy(removed_file_name):
    with tempfile.TemporaryDirectory() as tempfolder:
        shutil.copytree(
            "tests/data/001_source_simple_copy", os.path.join(tempfolder, "source")
        )
        os.unlink(os.path.join(tempfolder, "source", "rosi", removed_file_name))
        process(
            os.path.join(tempfolder, "source"),
            os.path.join(tempfolder, "result"),
            exist_ok=True,
        )
        assert folder_to_dict(os.path.join(tempfolder, "result")) == folder_to_dict(
            "tests/data/001_source_simple_copy_result"
        )


def test_concat_poem():
    with tempfile.TemporaryDirectory() as tempfolder:
        process("tests/data/002_concat_poem", tempfolder, exist_ok=True)
        assert folder_to_dict(tempfolder) == folder_to_dict(
            "tests/data/002_concat_poem_result"
        )


def test_concat_poem_overwrite():
    with tempfile.TemporaryDirectory() as tempfolder:
        process("tests/data/003_concat_poem_overwrite", tempfolder, exist_ok=True)
        assert folder_to_dict(tempfolder) == folder_to_dict(
            "tests/data/003_concat_poem_overwrite_result"
        )


def test_concat_poem_overwrite_external():
    with tempfile.TemporaryDirectory() as tempfolder:
        process(
            "tests/data/004_concat_poem_overwrite_external", tempfolder, exist_ok=True
        )
        assert folder_to_dict(tempfolder) == folder_to_dict(
            "tests/data/004_concat_poem_overwrite_external_result"
        )


@params_removed_file_name
def test_code(removed_file_name):
    with tempfile.TemporaryDirectory() as tempfolder:
        shutil.copytree("tests/data/005_code", os.path.join(tempfolder, "source"))
        os.unlink(os.path.join(tempfolder, "source", removed_file_name))
        process(
            os.path.join(tempfolder, "source"),
            os.path.join(tempfolder, "result"),
            exist_ok=True,
        )
        assert folder_to_dict(os.path.join(tempfolder, "result")) == folder_to_dict(
            "tests/data/005_code_result"
        )


@params_removed_file_name
def test_docker_svgo(removed_file_name):
    with tempfile.TemporaryDirectory() as tempfolder:
        shutil.copytree(
            "tests/data/006_docker_svgo", os.path.join(tempfolder, "source")
        )
        os.unlink(os.path.join(tempfolder, "source", removed_file_name))
        process(
            os.path.join(tempfolder, "source"),
            os.path.join(tempfolder, "result"),
            exist_ok=True,
        )

        assert folder_to_dict(os.path.join(tempfolder, "result")) == folder_to_dict(
            "tests/data/006_docker_svgo_result"
        )
