from acnestis.processing import BaseProcessor
from acnestis.steps import concat_files, copy_folder

PROCESSOR = BaseProcessor(
    [
        copy_folder("../poem_origin"),
        concat_files("poem.txt"),
    ],
    as_file="poem.txt",
)
