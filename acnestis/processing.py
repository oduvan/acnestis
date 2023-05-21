from typing import Callable, Iterable


class BaseProcessor:
    def __init__(self, steps: Iterable[Callable[[str], None]]) -> None:
        self.steps = steps

    def process(self, target: str):
        for step in self.steps:
            step(target)
