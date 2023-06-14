from acnestis.processing import Processor
from acnestis.steps import using_folder

PROCESSOR = Processor(
    [using_folder("../mike")],
)
