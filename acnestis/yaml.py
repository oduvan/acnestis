import yaml  # type: ignore[import]
from typing import Any

from .processing import BaseProcessor
from . import steps


def gen_processor(data: dict) -> BaseProcessor:
    data_steps = data.pop("steps", [])
    k_steps = []
    for step in data_steps:
        assert "name" in step, "Step must have a name"
        k_steps.append(getattr(steps, step.pop("name"))(**step))

    if "processors" in data:
        data["processors"] = [gen_processor(p) for p in data["processors"]]
    return BaseProcessor(k_steps, **data)


def main(code: str) -> Any:
    return gen_processor(yaml.safe_load(code))
