import yaml  # type: ignore[import]
from typing import Any

from .processing import Processor
from . import steps


def gen_processor(data: dict) -> Processor:
    data_steps = data.pop("steps", [])
    k_steps = []
    for step in data_steps:
        if "name" in step:
            k_steps.append(getattr(steps, step.pop("name"))(**step))
        else:
            k_steps.append(gen_processor(step))
    return Processor(k_steps, **data)


def main(code: str) -> Any:
    return gen_processor(yaml.safe_load(code))
