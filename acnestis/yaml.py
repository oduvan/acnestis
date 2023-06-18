import yaml  # type: ignore[import]
from typing import Any, Optional, Dict

from .processing import Processor
from . import steps


def gen_processor(data: dict, py_globals: Optional[Dict[str, Any]] = None) -> Processor:
    data_steps = data.pop("steps", [])
    k_steps = []
    for step in data_steps:
        if isinstance(step, str):
            assert py_globals is not None
            k_steps.append(py_globals[step])
        elif "name" in step:
            k_steps.append(getattr(steps, step.pop("name"))(**step))
        else:
            k_steps.append(gen_processor(step))
    return Processor(k_steps, **data)


def main(code: str, py_globals: Optional[Dict[str, Any]] = None) -> Any:
    return gen_processor(yaml.safe_load(code), py_globals=py_globals)
