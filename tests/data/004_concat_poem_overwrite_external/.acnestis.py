import os

from acnestis.processing import BaseProcessor
from acnestis.steps import copy_folder

PROCESSOR = BaseProcessor(
    [
        copy_folder(
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "002_concat_poem")
            )
        ),
    ],
)
