from typing import Callable, Iterable, Optional


class BaseProcessor:
    def __init__(
        self, steps: Iterable[Callable], replace_folder_with_file: Optional[str] = None
    ) -> None:
        self.steps = steps
        self.replace_folder_with_file = replace_folder_with_file

    def process(self, source_root: str, target: str):
        for step in self.steps:
            step(source_root, target)
