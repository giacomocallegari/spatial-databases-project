from typing import *

from src.geometry import Segment, Trapezoid


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


def split_trapezoids(s: Segment, deltas: List[Trapezoid]) -> (List[Trapezoid], List[Trapezoid]):
    """Splits the trapezoids intersected by a segment into their upper and lower parts.

    Args:
        s (Segment): The segment.
        deltas (List[Trapezoid]): The list of intersected trapezoids.

    Returns:
        (List[Trapezoid], List[Trapezoid]): The lists of the upper and lower parts of trapezoids, respectively.
    """

    upper = []
    lower = []

    # Add the leftmost trapezoids.
    upper.append(Trapezoid(deltas[0].top, s, s.p, deltas[0].rightp))
    lower.append(Trapezoid(s, deltas[0].bottom, s.p, deltas[0].rightp))

    # Add the intermediate trapezoids.
    for i in range(1, len(deltas) - 1):
        curr = deltas[i]
        upper.append(Trapezoid(curr.top, s, curr.leftp, curr.rightp))
        lower.append(Trapezoid(s, curr.bottom, curr.leftp, curr.rightp))

    # Add the rightmost trapezoids.
    upper.append(Trapezoid(deltas[-1].top, s, deltas[-1].leftp, s.q))
    lower.append(Trapezoid(s, deltas[-1].bottom, deltas[-1].leftp, s.q))

    return upper, lower


def merge_trapezoids(parts: List[Trapezoid]) -> List[Trapezoid]:
    """Merges the adjacent trapezoids that share both non-vertical sides.

    Args:
        parts (List[Trapezoid]): The list of parts of trapezoids.

    Returns:
        List[Trapezoid]: The list of merged trapezoids.
    """

    res = []

    i = 0
    j = 1
    size = len(parts)

    while i < size and j < size:
        # Initialize the properties of a new trapezoid.
        top = parts[i].top
        bottom = parts[i].bottom
        leftp = parts[i].leftp
        rightp = parts[i].rightp

        # Check if the current trapezoid can be merged with the predecessor.
        while (i < size and j < size) and (parts[j].top == parts[i].top and parts[j].bottom == parts[i].bottom):
            rightp = parts[j].rightp

            j += 1

        # Add the merged trapezoid to the list.
        res.append(Trapezoid(top, bottom, leftp, rightp))

        i = j

    return res


def update_neighbors(deltas: List[Trapezoid], ln: Trapezoid, rn: Trapezoid, above: bool) -> None:
    """Updates the neighbors of a list of trapezoids that share the same non-vertical side.

    Args:
        deltas (List[Trapezoids]): The list of adjacent trapezoids.
        ln: The left neighbor of the leftmost trapezoid.
        rn: The right neighbor of the rightmost trapezoid.
        above (bool): True if the trapezoids share the bottom side, False if they share the top side.
    """

    if len(deltas) > 1:
        # Set the neighbors of the leftmost trapezoid.
        if above:
            deltas[0].set_neighbors(ln, None, None, deltas[1])
        else:
            deltas[0].set_neighbors(None, ln, deltas[1], None)

        # Set the neighbors of the intermediate trapezoids.
        for i in range(1, len(deltas) - 1):
            pred = deltas[i - 1]
            curr = deltas[i]
            succ = deltas[i + 1]

            if above:
                curr.set_neighbors(None, pred, None, succ)
            else:
                curr.set_neighbors(pred, None, succ, None)

        # Set the neighbors of the rightmost trapezoid.
        if above:
            deltas[-1].set_neighbors(None, deltas[-2], rn, None)
        else:
            deltas[-1].set_neighbors(deltas[-2], None, None, rn)
    else:
        # Set the neighbors of the only trapezoid.
        if above:
            deltas[0].set_neighbors(ln, None, rn, None)
        else:
            deltas[0].set_neighbors(None, ln, None, rn)
