import os
from typing import Union, Dict, Any, NewType, TypeVar


NestedDict = NewType("NestedDict", Dict[str, Union[str, Any]])


def folder_to_dict(folder_path: str) -> NestedDict:
    result: NestedDict = {}  # type: ignore[assignment]
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            with open(item_path, "r") as file:
                result[item] = file.read()
        elif os.path.isdir(item_path):
            result[item] = folder_to_dict(item_path)
    return result
