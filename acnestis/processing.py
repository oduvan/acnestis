import os
from typing import Callable, Iterable, Optional


class BaseProcessor:
    def __init__(
        self,
        steps: Optional[Iterable[Callable]] = None,
        as_file: Optional[str] = None,
        folder: Optional[str] = None,
        processors: Optional[Iterable] = None,
    ) -> None:
        self.steps = steps
        self.as_file = as_file
        self.folder = folder
        self.processors = processors

    def process(self, source_root: str, target: str):
        if self.processors:
            for processor in self.processors:
                assert processor.folder is not None

                next_folder = target
                for ff in processor.folder.split("/"):
                    next_folder = os.path.join(next_folder, ff)
                    if not os.path.exists(next_folder):
                        os.mkdir(next_folder)

                processor.process(
                    os.path.join(source_root, *processor.folder.split("/")),
                    os.path.join(target, *processor.folder.split("/")),
                )
        if self.steps:
            for step in self.steps:
                step(source_root, target)
