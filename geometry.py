from typing import List


class Point:
    """Class for points.

    Attributes:
        x: The X coordinate.
        y: The Y coordinate.
    """

    def __init__(self, x: float, y: float) -> None:
        """Initializes Point with the coordinates."""
        self.x = x
        self.y = y


class Segment:
    """Class for segments.

    Attributes:
        p1: The first endpoint.
        p2: The second endpoint.
    """

    def __init__(self, p1: Point, p2: Point) -> None:
        """Initializes Segment with the list of endpoints."""
        self.p1 = p1
        self.p2 = p2


class Subdivision:
    """Class for subdivisions.

    Attributes:
        segments: The list of segments.
    """

    def __init__(self, segments: List[Segment]):
        """Initializes Subdivision with the list of segments."""
        self.segments = segments
