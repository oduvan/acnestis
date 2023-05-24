import tempfile
import os
import shutil

from acnestis.command import process

from .tools import folder_to_dict


def test_source_simple_copy():
    with tempfile.TemporaryDirectory() as tempfolder:
        shutil.copytree(
            "tests/data/001_source_simple_copy", os.path.join(tempfolder, "source")
        )
        os.unlink(os.path.join(tempfolder, "source", "rosi", ".acnestis.yaml"))
        process(
            os.path.join(tempfolder, "source"),
            os.path.join(tempfolder, "result"),
            exist_ok=True,
        )
        assert folder_to_dict(os.path.join(tempfolder, "result")) == folder_to_dict(
            "tests/data/001_source_simple_copy_result"
        )


def test_source_simple_copy_yaml():
    with tempfile.TemporaryDirectory() as tempfolder:
        shutil.copytree(
            "tests/data/001_source_simple_copy", os.path.join(tempfolder, "source")
        )
        os.unlink(os.path.join(tempfolder, "source", "rosi", ".acnestis.py"))
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
