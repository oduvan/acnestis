import yaml  # type: ignore[import]
from typing import Any

from .processing import BaseProcessor
from . import steps


def main(code: str) -> Any:
    data: Any = yaml.safe_load(code)
    data_steps = data.pop("steps", [])
    k_steps = []
    for step in data_steps:
        assert "name" in step, "Step must have a name"
        k_steps.append(getattr(steps, step.pop("name"))(**step))
    return BaseProcessor(k_steps, **data)
