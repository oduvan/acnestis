from acnestis.processing import Processor
from acnestis.steps import concat_files, using_folder

PROCESSOR = Processor(
    [
        using_folder("../poem_origin"),
        concat_files("poem.txt"),
    ],
    as_file="poem.txt",
)
