from acnestis.processing import BaseProcessor
from acnestis.steps import copy_folder


import os
import shutil


def duplicates_2(source_root, target):
    FILE_NAME = "input.txt"
    for i in range(3):
        shutil.copyfile(
            os.path.join(source_root, FILE_NAME),
            os.path.join(target, str(i) + "__" + FILE_NAME),
        )


PROCESSOR = BaseProcessor(
    [duplicates_2],
)
