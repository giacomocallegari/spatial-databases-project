from typing import *


def get_id(obj: Optional[object]) -> str:
    """Returns the ID of the object if not None, otherwise returns "None".

    Args:
        obj (Optional[object]): The object.

    Returns:
        str: The ID of the object or "None".
    """

    res = "None"

    if obj is not None:
        res = str(id(obj))

    return res
