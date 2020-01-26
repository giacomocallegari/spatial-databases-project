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

    def lies_left(self, p: "Point") -> bool:
        """Checks if the current point lies to the left of the given point.

        Args:
            p (Point): The other point.

        Returns:
            bool: True if the current point lies to the left, False otherwise.
        """

        return self.x < p.x

    def lies_above(self, s: "Segment") -> bool:
        """Checks if the point lies above the given segment.

        Args:
            s (Segment): The segment.

        Returns:
            bool: True if the point lies above, False otherwise.
        """

        x = self.x
        y = self.y
        px = s.p.x
        py = s.p.y
        qx = s.q.x
        qy = s.q.y

        v1 = (qx - px, qy - py)
        v2 = (qx - x, qy - y)

        # Compute the cross product between the vectors.
        xp = (v1[0] * v2[1]) - (v1[1] * v2[0])

        return xp <= 0


class Segment:
    """Class for segments.

    A segment is defined by its endpoints, which are specified from left to right.

    Attributes:
        p (Point): The leftmost endpoint.
        q (Point): The rightmost endpoint.
    """

    def __init__(self, p1: Point, p2: Point) -> None:
        """Initializes a Segment object.

        Args:
            p1 (Point): The first endpoint.
            p2 (Point): The second endpoint.
        """

        # Initialize the endpoints from left to right.
        if p1.x < p2.x:
            self.p = p1
            self.q = p2
        else:
            self.p = p2
            self.q = p1

    def __str__(self) -> str:
        """Returns the string representation of a Segment object.
        """

        # res = "p = " + str(self.p) + "\t\tq = " + str(self.q)
        res = str(self.p) + "--------" + str(self.q)

        return res


class Trapezoid:
    """Class for trapezoids.

    Attributes:
        top (Segment): The top non-vertical segment.
        bottom (Segment): The bottom non-vertical segment.
        leftp (Point): The left generator endpoint.
        rightp (Point): The right generator endpoint.
        uln (Optional[Trapezoid]): The upper left neighbor.
        lln (Optional[Trapezoid]): The lower left neighbor.
        urn (Optional[Trapezoid]): The upper right neighbor.
        lrn (Optional[Trapezoid]): The lower right neighbor.
        leaf (LeafNode): The corresponding leaf.
    """

    def __init__(self, top: Segment, bottom: Segment, leftp: Point, rightp: Point) -> None:
        """Initializes a Trapezoid object.

        Args:
            top (Segment): The top non-vertical segment.
            bottom (Segment): The bottom non-vertical segment.
            leftp (Point): The left generator endpoint.
            rightp (Point): The right generator endpoint.
        """

        from src.nodes import LeafNode

        self.top = top
        self.bottom = bottom
        self.leftp = leftp
        self.rightp = rightp

        self.uln = None
        self.lln = None
        self.urn = None
        self.lrn = None

        self.leaf = LeafNode(self)

    def __str__(self) -> str:
        """Returns the string representation of a Trapezoid object.
        """

        from src.util import get_id

        res = ""
        res += "\tTrapezoid ID: " + get_id(self) + "\t| Leaf ID: " + get_id(self.leaf) + "\n"
        res += "\ttop:\t" + str(self.top) + "\n"
        res += "\tbottom:\t" + str(self.bottom) + "\n"
        res += "\tleftp = " + str(self.leftp) + "\trightp = " + str(self.rightp) + "\n"
        res += "\tuln = " + get_id(self.uln) + "\turn = " + get_id(self.urn) + "\n"
        res += "\tlln = " + get_id(self.lln) + "\tlrn = " + get_id(self.lrn) + "\n"

        return res

    def set_neighbors(self, uln: Optional["Trapezoid"], lln: Optional["Trapezoid"],
                      urn: Optional["Trapezoid"], lrn: Optional["Trapezoid"]) -> None:
        """Sets the neighbors of the trapezoid.

        Args:
            uln: The upper left neighbor.
            lln: The lower left neighbor.
            urn: The upper right neighbor.
            lrn: The lower right neighbor.
        """

        # Update the neighbors of the current node.
        self.uln = uln
        self.lln = lln
        self.urn = urn
        self.lrn = lrn

        # Notify the neighbors of this update.
        if uln is not None:
            uln.urn = self
        if lln is not None:
            lln.lrn = self
        if urn is not None:
            urn.uln = self
        if lrn is not None:
            lrn.lln = self
