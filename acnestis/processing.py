from typing import Callable, Iterable, Optional


class BaseProcessor:
    def __init__(
        self, steps: Iterable[Callable], as_file: Optional[str] = None
    ) -> None:
        self.steps = steps
        self.as_file = as_file

    def process(self, source_root: str, target: str):
        for step in self.steps:
            step(source_root, target)
