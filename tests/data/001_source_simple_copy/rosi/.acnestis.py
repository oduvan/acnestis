from acnestis.processing import BaseProcessor
from acnestis.steps import copy_folder

PROCESSOR = BaseProcessor(
    [copy_folder("../mike")],
)
