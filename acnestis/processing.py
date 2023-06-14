import os
from typing import Any, Callable, Iterable, Optional


class Processor:
    def __init__(
        self,
        steps: Iterable[Callable],
        as_file: Optional[str] = None,
        folder: Optional[str] = None,
    ) -> None:
        self.steps = steps
        self.as_file = as_file
        self.folder = folder

    def process(self, source_root: str, target: str):
        if self.folder:
            next_folder: str = target
            for ff in self.folder.split("/"):
                next_folder = os.path.join(next_folder, ff)
                if not os.path.exists(next_folder):
                    os.mkdir(next_folder)

            source_root = os.path.join(source_root, *self.folder.split("/"))
            target = os.path.join(target, *self.folder.split("/"))

        for step in self.steps:
            step(source_root, target)

    def __call__(self, *args: Any, **kwargs: Any):
        self.process(*args, **kwargs)
