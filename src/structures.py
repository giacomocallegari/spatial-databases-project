import random
from typing import *

from src.geometry import Segment, Point, Trapezoid
from src.nodes import Node, XNode, YNode, LeafNode


class TrapezoidalMap:
    """Class for trapezoidal maps.

    A trapezoidal map is a refinement of a subdivision, obtained by drawing for each segment endpoint vertical
    extensions that stop at the first non-vertical segment.
    Every element of the map is a trapezoid, or a triangle in the degenerate case. The structure is therefore
    represented as a set of Trapezoid objects.
    The whole map is enclosed in a bounding box, which is a rectangle.

    Attributes:
        trapezoids (Set[Trapezoids]): The set of trapezoids.
        D (SearchStructure): The search structure.
    """

    def __init__(self, R: Trapezoid) -> None:
        """Initializes a TrapezoidalMap object.

        Args:
            R (Trapezoid): The bounding box rectangle.
        """

        print("Initializing the trapezoidal map...")

        # Create the set of trapezoids and add the bounding box.
        self.trapezoids = set()
        self.add_trapezoid(R)

        # Create the search structure.
        self.D = SearchStructure(R)

    def __str__(self) -> str:
        """Returns the string representation of a TrapezoidalMap object.
        """

        res = ""

        for trapezoid in self.trapezoids:
            res += str(trapezoid)

        return res

    def add_trapezoid(self, trapezoid: Trapezoid) -> None:
        """Adds a trapezoid to the trapezoidal map.

        Args:
            trapezoid (Trapezoid): The trapezoid to add.
        """

        self.trapezoids.add(trapezoid)

    def remove_trapezoid(self, trapezoid: Trapezoid) -> None:
        """Removes a trapezoid from the trapezoidal map.

        Args:
            trapezoid (Trapezoid): The trapezoid to remove.
        """

        self.trapezoids.remove(trapezoid)

    def follow_segment(self, s: Segment) -> List[Trapezoid]:  # TODO
        """Finds the trapezoids that are intersected by a segment.

        The search starts from the leftmost intersected trapezoid, obtained by querying the left endpoint of the segment
        on the current search structure. Then, iteratively, the right neighbor of each intersected trapezoid is found
        until the right endpoint is reached.
        The result is the list of intersected trapezoids, ordered from left to right.

        Args:
            s (Segment): The segment.

        Returns:
            List[Trapezoid]: The list of intersected trapezoids.
        """

        # Initialize the list of trapezoids.
        deltas = list()

        # Get the endpoints of the segment.
        p, q = s.p, s.q

        # Find the first intersected trapezoid.
        deltas.append(self.D.query(p))

        # Iteratively find the next intersected trapezoids.
        j = 0
        while deltas[j].rightp.lies_left(q):
            if deltas[j].rightp.lies_above(s):
                # Select the lower right neighbor.
                deltas[j + 1] = deltas[j].lrn
            else:
                # Select the upper right neighbor.
                deltas[j + 1] = deltas[j].urn

            j += 1

        return deltas

    def merge(self, parts: List[Trapezoid]) -> List[Trapezoid]:
        """Merges the adjacent trapezoids that share both non-vertical sides.

        Args:
            parts (List[Trapezoid]): The list of parts of trapezoids.

        Returns:
            List[Trapezoid]: The list of merged trapezoids.
        """

        i = 1
        res = []

        # Iterate on all original trapezoids.
        while i < len(parts):
            pred = parts[i - 1]
            curr = parts[i]

            # Initialize the properties of a new merged trapezoid.
            top = pred.top
            bottom = pred.bottom
            leftp = pred.leftp
            rightp = None
            uln = pred.uln
            lln = pred.lln
            urn = None
            lrn = None

            # Keep merging adjacent trapezoids that share both non-vertical sides.
            while curr.top == pred.top and curr.bottom == pred.bottom and i < len(parts):
                rightp = curr.rightp
                urn = curr.urn
                lrn = curr.lrn

                curr = parts[i + 1]

            # Add the merged trapezoid to the list.
            merged = Trapezoid(top, bottom, leftp, rightp)
            merged.set_neighbors(uln, lln, urn, lrn)
            res.append(merged)

        return res

    def update(self, s: Segment, deltas: List[Trapezoid]) -> None:  # TODO
        """Updates the trapezoidal map after some trapezoids have been intersected by the segment.

        The intersected trapezoids are removed and replaced with the new ones.

        Args:
            s (Segment): The segment.
            deltas (List[Trapezoids]): The list of intersected trapezoids.
        """

        # Remove the intersected trapezoids.
        # for trapezoid in deltas:
        #     self.remove_trapezoid(trapezoid)

        # Check whether one or more trapezoids have been intersected.
        if len(deltas) == 1:
            # Get the single intersected trapezoid.
            old = deltas[0]

            # Generate the new trapezoids.
            A = Trapezoid(old.top, old.bottom, old.leftp, s.p)
            B = Trapezoid(old.top, old.bottom, s.q, old.rightp)
            C = Trapezoid(old.top, s, s.p, s.q)
            D = Trapezoid(s, old.bottom, s.p, s.q)

            # Set the neighbors of the new trapezoids.
            A.set_neighbors(old.uln, old.lln, C, D)
            B.set_neighbors(C, D, old.urn, old.lrn)
            C.set_neighbors(A, None, B, None)
            D.set_neighbors(None, A, None, B)

            # Add the new trapezoids and remove the old one.
            self.remove_trapezoid(old)
            self.trapezoids = self.trapezoids.union({A, B, C, D})
        else:
            # TODO: Case where the segment's vertex is an existing endpoint
            # Create the leftmost and rightmost new trapezoids.
            first = Trapezoid(deltas[0].top, deltas[0].bottom, deltas[0].leftp, s.p)
            last = Trapezoid(deltas[-1].top, deltas[-1].bottom, s.q, deltas[-1].rightp)

            # Create the lists for the upper and the lower parts of the intersected trapezoids.
            upper = []
            lower = []

            # Split each intersected trapezoid into its upper and lower parts.
            upper.append(Trapezoid(first.top, s, s.p, first.rightp))
            lower.append(Trapezoid(s, first.bottom, s.p, first.rightp))
            for i in range(1, len(deltas) - 1):
                curr = deltas[i]
                upper.append(Trapezoid(curr.top, s, curr.leftp, curr.rightp))
                lower.append(Trapezoid(s, curr.bottom, curr.leftp, curr.rightp))
            upper.append(Trapezoid(last.top, s, last.leftp, s.q))
            lower.append(Trapezoid(s, last.bottom, last.leftp, s.q))

            # Merge the upper and the lower parts where possible.
            upper = self.merge(upper)
            lower = self.merge(lower)

            # Set the neighbors of each trapezoid.
            first.set_neighbors(deltas[0].uln, deltas[0].lln, upper[0], lower[0])
            upper[0].set_neighbors(None, None, None, upper[1])
            for i in range(1, len(upper) - 1):
                pred = upper[i - 1]
                curr = upper[i]
                succ = upper[i + 1]
                curr.set_neighbors(None, pred, None, succ)
            upper[-1].set_neighbors(None, upper[-2], None, None)
            lower[0].set_neighbors(None, None, lower[1], None)
            for i in range(1, len(lower) - 1):
                pred = lower[i - 1]
                curr = lower[i]
                succ = lower[i + 1]
                curr.set_neighbors(pred, None, succ, None)
            lower[-1].set_neighbors(lower[-2], None, None, None)
            last.set_neighbors(upper[-1], lower[-1], deltas[-1].urn, deltas[-1].lrn)

            # Add the new trapezoids to the map.
            self.add_trapezoid(first)
            for trapezoid in upper:
                self.add_trapezoid(trapezoid)
            for trapezoid in lower:
                self.add_trapezoid(trapezoid)
            self.add_trapezoid(last)

        self.D.update(self, s, deltas)


class SearchStructure:
    """Class for the search structure.

    The search structure is a directed acyclic graph (DAG) used to query the location of points in trapezoids.
    All inner nodes have an out-degree of exactly 2 and can be X-nodes (endpoints) or Y-nodes (segments). Each leaf of
    the DAG represents a trapezoid.

    Attributes:
        nodes (Set[Node]): The set of nodes.
        root (Node): The root of the directed acyclic graph.
    """

    def __init__(self, R: Trapezoid) -> None:
        """Initializes a SearchStructure object.

        Args:
            R (Trapezoid): The bounding box rectangle.
        """

        print("Initializing the search structure...")

        self.nodes = set()

        # Create the root and add it to the set of nodes.
        self.root = LeafNode(R)
        self.add_node(self.root)

    def __str__(self) -> str:
        """Returns the string representation of a SearchStructure object.
        """

        res = "root:" + str(self.root)

        return res

    def add_node(self, node: Node) -> None:
        """Adds a node to the set of the search structure.

        Args:
            node: The node to add.
        """

        self.nodes.add(node)

    def remove_node(self, node: Node) -> None:
        """Removes a node from the set of the search structure.

        Args:
            node: The node to remove.
        """

        for member in self.nodes:
            if node == member.left:
                member.set_left_child(None)
            elif node == member.right:
                member.set_right_child(None)

        self.nodes.remove(node)

    def update(self, T: TrapezoidalMap, s: Segment, deltas: List[Trapezoid]) -> None:  # TODO
        """Updates the search structure after some trapezoids have been intersected by the segment.

        The leaves of intersected trapezoids are removed and replaced with the ones of the new trapezoids, also adding
        some inner nodes.

        Args:
            T (TrapezoidalMap): The corresponding trapezoidal map.
            s (Segment): The segment.
            deltas (List[Trapezoid]): The list of intersected trapezoids.
        """

        # Remove the leaves of the intersected trapezoids.
        for trapezoid in deltas:
            leaf = self.nodes.get(id(trapezoid))
            self.remove_node(leaf)

        # Check the number of intersected trapezoids.
        if len(deltas) == 1:
            print("Single trapezoid")

            parent = self.nodes.get(id(deltas[0]))  # TODO

            # Get the new trapezoids.
            A, B, C, D = T.trapezoids  # TODO

            # Add the leaves of the new trapezoids.
            nA = LeafNode(A)
            nB = LeafNode(B)
            nC = LeafNode(C)
            nD = LeafNode(D)
            self.add_node(nA)
            self.add_node(nB)
            self.add_node(nC)
            self.add_node(nD)

            # Add the inner nodes.
            np = XNode(s.p)
            nq = XNode(s.q)
            ns = YNode(s)
            self.add_node(np)
            self.add_node(nq)
            self.add_node(ns)

            # Add the edges.
            parent.set_left_child()
            parent.set_right_child()
            np.set_left_child(nA)
            np.set_right_child(nq)
            nq.set_left_child(ns)
            nq.set_right_child(nB)
            ns.set_left_child(nC)
            ns.set_right_child(nD)

        else:  # TODO
            print("Multiple trapezoids")

    def query(self, q: Point) -> Optional[Trapezoid]:
        """Queries a point in the search structure.

        Querying a point consists in a recursive traversal of the search structure's DAG, from the root to a leaf.
        Once the trapezoid has been obtained, the corresponding face of the original subdivision can be found.

        Args:
            q (Point): The query point.

        Returns:
            Optional[Trapezoid]: The trapezoid that contains the query point.
        """

        # Start from the root of the search structure.
        node = self.root

        # Traverse the search structure until a leaf is reached.
        face = node.traverse(q)

        return face


class Subdivision:
    """Class for subdivisions.

    A subdivision is a set of non-crossing segments that divide a plane. These segments can have common endpoints.

    Attributes:
        segments (List[Segment]): The list of segments.
        T (TrapezoidalMap): The trapezoidal map.
    """

    def __init__(self, segments: List[Segment]) -> None:
        """Initializes a Subdivision object.

        Args:
            segments (List[Segment]): The list of segments.
        """

        self.segments = segments
        self.T = None

    def __str__(self) -> str:
        """Returns the string representation of a Subdivision object.
        """

        res = ""

        for i in range(len(self.segments)):
            res += "Segment " + str(i) + ":\n"
            res += str(self.segments[i]) + "\n"

        return res

    def bounding_box(self) -> Trapezoid:
        """Creates a bounding box for the subdivision.

        The bounding box is a rectangle that contains the whole subdivision, producing a bounded area where a
        trapezoidal map refinement can be applied.
        The extreme X and Y coordinates of the subdivision are obtained and, after applying a fixed margin of 1 to all
        sides, the rectangle is built.

        Returns:
            Trapezoid: The bounding box rectangle, a particular case of trapezoid.
        """

        print("Building the bounding box...")

        min_x = float("inf")
        max_x = float("-inf")
        min_y = float("inf")
        max_y = float("-inf")

        # Iterate on every segment of the subdivision.
        for segment in self.segments:
            p = segment.p
            q = segment.q

            # Set the horizontal extremes. The endpoints of each segment are ordered from left to right.
            if p.x < min_x:
                min_x = p.x
            elif q.x > max_x:
                max_x = q.x

            # Set the vertical extremes.
            if p.y < min_y:
                min_y = p.y
            elif p.y > max_y:
                min_y = p.y
            if q.y < min_y:
                min_y = q.y
            elif q.y > max_y:
                max_y = q.y

        # Get the extreme coordinates of the subdivision and add a margin of 1 to each side.
        x1 = min_x - 1
        x2 = max_x + 1
        y1 = min_y - 1
        y2 = max_y + 1

        # Set the corners of the rectangle.
        ll = Point(x1, y1)
        lr = Point(x2, y1)
        ul = Point(x1, y2)
        ur = Point(x2, y2)

        # Create and return the bounding box.
        return Trapezoid(Segment(ul, ur), Segment(ll, lr), ll, lr)

    def trapezoidal_map(self) -> None:
        """Creates the trapezoidal map from the subdivision.

        The trapezoidal map is a refinement of the original subdivision. It is completed by a search structure, which is
        a DAG representing the trapezoids as leaves.
        These structures can be used together to query which trapezoid contains a given point.
        """

        # Create the bounding box.
        R = self.bounding_box()
        # print(str(R))

        # Initialize the trapezoidal map.
        T = TrapezoidalMap(R)
        # print(str(T))

        # Shuffle the segments of the subdivision.
        segments = self.segments.copy()
        random.shuffle(segments)  # TODO: support customizable seed

        # Iteratively build the trapezoidal map.
        for i in range(len(segments)):
            # Find the intersected trapezoids.
            delta = self.T.follow_segment(segments[i])

            # Update the trapezoidal map.
            self.T.update(segments[i], delta)
