import tempfile

from acnestis.command import process

from .tools import folder_to_dict


def test_source_simple_copy():
    with tempfile.TemporaryDirectory() as tempfolder:
        result_folder = folder_to_dict("tests/data/001_source_simple_copy_result")
        process("tests/data/001_source_simple_copy", tempfolder, exist_ok=True)
        assert folder_to_dict(tempfolder) == result_folder


def test_concat_poem():
    with tempfile.TemporaryDirectory() as tempfolder:
        result_folder = folder_to_dict("tests/data/002_concat_poem_result")
        process("tests/data/002_concat_poem", tempfolder, exist_ok=True)
        assert folder_to_dict(tempfolder) == result_folder
