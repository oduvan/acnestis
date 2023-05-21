from acnestis.processing import BaseProcessor
from acnestis.steps import concat_files

PROCESSOR = BaseProcessor(
    [concat_files("poem.txt")], replace_folder_with_file="poem.txt"
)
