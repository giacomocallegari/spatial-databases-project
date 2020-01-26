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

    The resulting trapezoids maintain the relevant neighbors that will be used to initialize the merged trapezoids.

    Args:
        s (Segment): The segment.
        deltas (List[Trapezoid]): The list of intersected trapezoids.

    Returns:
        (List[Trapezoid], List[Trapezoid]): The lists of the upper and lower parts of trapezoids, respectively.
    """

    upper = []
    lower = []

    # Add the leftmost trapezoids.
    left_upper = Trapezoid(deltas[0].top, s, s.p, deltas[0].rightp)
    left_upper.set_neighbors(None, None, deltas[0].urn, None)
    upper.append(left_upper)
    left_lower = Trapezoid(s, deltas[0].bottom, s.p, deltas[0].rightp)
    left_lower.set_neighbors(None, None, None, deltas[0].lrn)
    lower.append(left_lower)

    # Add the intermediate trapezoids.
    for i in range(1, len(deltas) - 1):
        # Get the intersected trapezoid.
        curr = deltas[i]

        # Split the trapezoid.
        curr_upper = Trapezoid(curr.top, s, curr.leftp, curr.rightp)
        curr_upper.set_neighbors(curr.uln, None, curr.urn, None)
        upper.append(curr_upper)
        curr_lower = Trapezoid(s, curr.bottom, curr.leftp, curr.rightp)
        curr_lower.set_neighbors(None, curr.lln, None, curr.lrn)
        lower.append(curr_lower)

    # Add the rightmost trapezoids.
    right_upper = Trapezoid(deltas[-1].top, s, deltas[-1].leftp, s.q)
    right_upper.set_neighbors(deltas[-1].uln, None, None, None)
    upper.append(right_upper)
    right_lower = Trapezoid(s, deltas[-1].bottom, deltas[-1].leftp, s.q)
    right_lower.set_neighbors(None, deltas[-1].lln, None, None)
    lower.append(right_lower)

    return upper, lower


def merge_trapezoids(parts: List[Trapezoid]) -> List[Trapezoid]:
    """Merges the adjacent trapezoids that share both non-vertical sides.

    In the resulting list, the i-th element specifies the destination trapezoid of the i-th part, which means that the
    list contains duplicates for consecutive merged parts.

    Args:
        parts (List[Trapezoid]): The list of parts of trapezoids.

    Returns:
        List[Trapezoid]: The mapping from the original trapezoids to the merged ones.
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

        # Map each original trapezoid to the merged one.
        merged = Trapezoid(top, bottom, leftp, rightp)
        for k in range(i, j):
            res.append(merged)

        i = j

    return res


def update_neighbors(s_list: List[Trapezoid], m_list: List[Trapezoid], first: Trapezoid, last: Trapezoid,
                     above: bool) -> None:
    """Updates the neighbors of a list of trapezoids that share the same non-vertical side.

    Args:
        m_list (List[Trapezoids]): The mapping from the split trapezoids to the merged ones.
        s_list (List[Trapezoids]): The list of split trapezoids.
        first (Trapezoid): The leftmost neighbor.
        last (Trapezoid): The rightmost neighbor.
        above (bool): True if the trapezoids share the bottom side, False if they share the top side.
    """

    k = 0
    size = len(m_list)

    while k < size:
        old = s_list[k]
        curr = m_list[k]

        pred = m_list[k - 1] if k > 0 else None
        succ = curr

        # Iterate while the successor is a duplicate of the current trapezoid.
        while curr == succ:
            k += 1
            succ = m_list[k] if k < size else None

        # Check whether the upper or the lower trapezoids are being addressed.
        if above:
            uln = old.uln if k > 0 else first
            lln = pred
            urn = old.urn if k < size - 1 else last
            lrn = succ
        else:
            uln = pred
            lln = old.lln if k > 0 else first
            urn = succ
            lrn = old.lrn if k < size - 1 else last

        # Set the neighbors of the current trapezoid.
        curr.set_neighbors(uln, lln, urn, lrn)
