import random
from typing import *

from src.geometry import Segment, Point, Trapezoid
from src.nodes import Node, XNode, YNode, LeafNode
from src.util import *


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

        self.trapezoids.discard(trapezoid)

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
        curr = self.D.query(p)
        deltas.append(curr)

        # Iteratively find the next intersected trapezoids.
        while curr.rightp.lies_left(q):
            # Select the upper or lower right neighbor.
            if curr.rightp.lies_above(s):
                deltas.append(curr.lrn)
            else:
                deltas.append(curr.urn)

            # Get the last element of the list.
            curr = deltas[-1]

        """j = 0
        while deltas[j].rightp.lies_left(q):
            print(deltas)
            print("j: " + str(j))

            if deltas[j].rightp.lies_above(s):
                # Select the lower right neighbor.
                deltas[j + 1] = deltas[j].lrn
            else:
                # Select the upper right neighbor.
                deltas[j + 1] = deltas[j].urn

            j += 1"""

        return deltas

    def update(self, s: Segment, deltas: List[Trapezoid]) -> None:  # TODO
        """Updates the trapezoidal map after some trapezoids have been intersected by the segment.

        The intersected trapezoids are removed and replaced with the new ones.

        Args:
            s (Segment): The segment.
            deltas (List[Trapezoids]): The list of intersected trapezoids.
        """

        print("\nUpdating the trapezoidal map...", end=" ")

        # Check whether one or more trapezoids have been intersected.
        if len(deltas) == 1:
            print("Single trapezoid detected.")

            # Get the single intersected trapezoid.
            old = deltas[0]

            # Generate the new trapezoids.
            A = Trapezoid(old.top, old.bottom, old.leftp, s.p)  # Leftmost trapezoid
            B = Trapezoid(old.top, old.bottom, s.q, old.rightp)  # Rightmost trapezoid
            C = Trapezoid(old.top, s, s.p, s.q)  # Upper trapezoid
            D = Trapezoid(s, old.bottom, s.p, s.q)  # Lower trapezoid

            # Set the neighbors of the new trapezoids.
            A.set_neighbors(old.uln, old.lln, C, D)
            B.set_neighbors(C, D, old.urn, old.lrn)
            C.set_neighbors(A, None, B, None)
            D.set_neighbors(None, A, None, B)

            # Remove the old trapezoid and add the new ones.
            new_deltas = [A, B, C, D]
            self.remove_trapezoid(old)
            self.trapezoids = self.trapezoids.union(set(new_deltas))
        else:
            print("Multiple trapezoids detected.")

            # Split the intermediate intersected trapezoids into their upper and lower parts.
            print("Splitting the intermediate trapezoids...")
            upper, lower = split_trapezoids(s, deltas)

            # Merge the upper and the lower parts where possible.
            print("Merging the upper parts...")
            upper = merge_trapezoids(upper)
            print("Merging the lower parts...")
            lower = merge_trapezoids(lower)

            # Create the leftmost and rightmost new trapezoids.
            first = Trapezoid(deltas[0].top, deltas[0].bottom, deltas[0].leftp, s.p)
            first.set_neighbors(deltas[0].uln, deltas[0].lln, upper[0], lower[0])
            last = Trapezoid(deltas[-1].top, deltas[-1].bottom, s.q, deltas[-1].rightp)
            last.set_neighbors(upper[-1], lower[-1], deltas[-1].urn, deltas[-1].lrn)

            # Set the neighbors of each merged trapezoid.
            update_neighbors(upper, first, last, True)
            update_neighbors(lower, first, last, False)

            print("\n\nUPPER TRAPEZOIDS")
            for delta in upper:
                print(delta)

            print("\n\nLOWER TRAPEZOIDS")
            for delta in lower:
                print(delta)

            # Add the new trapezoids to the map.
            self.add_trapezoid(first)
            for trapezoid in upper:
                self.add_trapezoid(trapezoid)
            for trapezoid in lower:
                self.add_trapezoid(trapezoid)
            self.add_trapezoid(last)

            # TODO: generate new_deltas
            new_deltas = []

        # Update the search structure.
        self.D.update(s, deltas, new_deltas)


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
        self.root = R.leaf
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
            elif node in member.parents:
                member.remove_parent(node)

        self.nodes.discard(node)

    def update(self, s: Segment, old_ts: List[Trapezoid], new_ts: List[Trapezoid]) -> None:
        """Updates the search structure after some trapezoids have been intersected by the segment.

        The leaves of intersected trapezoids are removed and replaced with the ones of the new trapezoids, also adding
        some inner nodes.

        Args:
            s (Segment): The segment.
            old_ts (List[Trapezoid]): The list of intersected trapezoids.
            new_ts (List[Trapezoid]): The list of new trapezoids.
        """

        print("\nUpdating the search structure...")

        print("Intersected trapezoids:")
        for delta in old_ts:
            print(str(delta))

        print("New trapezoids:")
        for delta in new_ts:
            print(str(delta))

        # Check the number of intersected trapezoids.
        if len(old_ts) == 1:
            # print("Single trapezoid")

            # Get the parents of the old trapezoid's node.
            old = old_ts[0].leaf
            print("Node to replace:\n" + str(old))

            # Get the new trapezoids.
            A, B, C, D = new_ts

            # Create the inner nodes.
            np = XNode(s.p)
            nq = XNode(s.q)
            ns = YNode(s)

            # Add the edges.
            if self.root == old:
                self.root = np
            else:
                for parent in old.parents:
                    if parent.left_child == old:
                        parent.set_left_child(np)
                    elif parent.right_child == old:
                        parent.set_right_child(np)
            np.set_left_child(A.leaf)
            np.set_right_child(nq)
            nq.set_left_child(ns)
            nq.set_right_child(B.leaf)
            ns.set_left_child(C.leaf)
            ns.set_right_child(D.leaf)

        else:  # TODO
            # print("Multiple trapezoids")

            """# Manage the first intersected trapezoid.
            np = XNode(s.p)
            # self.add_node(np)  # TODO: check degenerate case
            old = old_ts[0].leaf
            parents = old.parents
            n_first = LeafNode()

            # Iterate through the intersected trapezoids.
            for i in range(1, len(old_ts) - 1):
                # Get the parents of the old trapezoid's node.
                old = old_ts[i].leaf
                parents = old.parents

                # Add the leaves of the new trapezoids.

                # Add the inner nodes.
                ns = YNode(s)
                # self.add_node(ns)
                if i == 0:
                    np = XNode(s.p)
                    # self.add_node(np)
                elif i == len(old_ts) - 1:
                    nq = XNode(s.p)
                    # self.add_node(nq)

                # Add the edges.
                for parent in parents:
                    if parent.left_child == old:
                        parent.set_left_child(ns)
                    elif parent.right_child == old:
                        parent.set_right_child(ns)"""

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
        segments (Set[Segment]): The list of segments.
        T (TrapezoidalMap): The trapezoidal map.
    """

    def __init__(self, segments: Set[Segment]) -> None:
        """Initializes a Subdivision object.

        Args:
            segments (Set[Segment]): The list of segments.
        """

        self.segments = segments

        # Create the bounding box.
        R = self.bounding_box()
        # print(str(R))

        # Initialize the trapezoidal map.
        self.T = TrapezoidalMap(R)
        # print(str(T))

    def __str__(self) -> str:
        """Returns the string representation of a Subdivision object.
        """

        res = ""

        for segment in self.segments:
            res += str(segment) + "\n"

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

        # Iterate through every segment of the subdivision.
        for segment in self.segments:
            p = segment.p
            q = segment.q

            # Set the horizontal extremes. The endpoints of each segment are ordered from left to right.
            if p.x < min_x:
                min_x = p.x
            if q.x > max_x:
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
        """Builds the trapezoidal map from the subdivision.

        The trapezoidal map is a refinement of the original subdivision. It is completed by a search structure, which is
        a DAG representing the trapezoids as leaves.
        These structures can be used together to query which trapezoid contains a given point.
        """

        # TODO: reset existing trapezoidal map?

        # Get the list of segments and shuffle it.
        segments = list(self.segments)
        # random.shuffle(segments)

        # Iteratively build the trapezoidal map.
        for i in range(len(segments)):
            print("\n" + 80 * "~")
            print("\tITERATION " + str(i) + ":\t" + str(segments[i]) + "\n")

            # Find the intersected trapezoids.
            deltas = self.T.follow_segment(segments[i])

            # Update the trapezoidal map.
            self.T.update(segments[i], deltas)
