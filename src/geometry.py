from typing import *


class Point:
    """Class for points.

    A point is represented by its X and Y coordinates.

    Attributes:
        x (float): The X coordinate.
        y (float): The Y coordinate.
    """

    def __init__(self, x: float, y: float) -> None:
        """Initializes a Point object.

        Args:
            x (float): The X coordinate.
            y (float): The Y coordinate.
        """

        self.x = x
        self.y = y

    def __str__(self) -> str:
        """Returns the string representation of a Point object.
        """

        res = "(" + str(self.x) + ", " + str(self.y) + ")"

        return res

    def lies_right(self, p: "Point") -> bool:
        """Checks if the current point lies to the right of the given point.

        Args:
            p (Point): The other point.

        Returns:
            bool: True if the current point lies to the right, False otherwise.
        """

        return self.x > p.x

    def lies_above(self, s: "Segment") -> bool:
        """Checks if the point lies above the given segment.

        Args:
            s (Segment): The segment.

        Returns:
            bool: True if the point lies above, False otherwise.
        """

        x = self.x
        y = self.y
        x1 = s.p1.x
        y1 = s.p1.y
        x2 = s.p2.x
        y2 = s.p2.y

        v1 = (x2 - x1, y2 - y1)
        v2 = (x2 - x, y2 - y)

        xp = (v1[0] * v2[1]) - (v1[1] * v2[0])

        return xp > 0


class Segment:
    """Class for segments.

    A segment is defined from its endpoints, which must be specified from left to right.

    Attributes:
        p1 (Point): The first endpoint (leftmost).
        p2 (Point): The second endpoint (rightmost).
    """

    def __init__(self, p1: Point, p2: Point) -> None:
        """Initializes a Segment object.

        Args:
            p1 (Point): The leftmost endpoint.
            p2 (Point): The rightmost endpoint.
        """

        self.p1 = p1
        self.p2 = p2

    def __str__(self) -> str:
        """Returns the string representation of a Segment object.
        """

        # res = "p1 = " + str(self.p1) + "\t\tp2 = " + str(self.p2)
        res = str(self.p1) + "--------" + str(self.p2)

        return res


class Subdivision:
    """Class for subdivisions.

    A subdivision is a set of segments that divide a plane. These segments can have common endpoints.

    Attributes:
        segments (List[Segment]): The list of segments.
    """

    def __init__(self, segments: List[Segment]) -> None:
        """Initializes a Segment object.

        Args:
            segments (List[Segment]): The list of segments.
        """

        self.segments = segments
        self.min_x = float("inf")
        self.max_x = float("-inf")
        self.min_y = float("inf")
        self.max_y = float("-inf")

        # Set the extremes of the subdivision.
        self.min_max()

    def __str__(self) -> str:
        """Returns the string representation of a Subdivision object.
        """

        res = ""

        for i in range(len(self.segments)):
            res += "Segment " + str(i) + ":\n"
            res += str(self.segments[i]) + "\n"

        return res

    def min_max(self) -> None:
        """Sets the minimum and maximum X and Y coordinates of the subdivision.

        These coordinates are obtained by checking every segment of the subdivision.
        """

        # Iterate on every segment of the subdivision.
        for segment in self.segments:
            p1 = segment.p1
            p2 = segment.p2

            # Set the horizontal extremes. The endpoints of each segment are ordered by the X coordinate.
            if p1.x < self.min_x:
                self.min_x = p1.x
            elif p2.x > self.max_x:
                self.max_x = p2.x

            # Set the vertical extremes.
            if p1.y < self.min_y:
                self.min_y = p1.y
            elif p1.y > self.max_y:
                self.min_y = p1.y
            if p2.y < self.min_y:
                self.min_y = p2.y
            elif p2.y > self.max_y:
                self.max_y = p2.y
