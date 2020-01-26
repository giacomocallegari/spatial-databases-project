import random
from typing import *

from src.geometry import Segment, Point, Trapezoid
from src.nodes import Node, XNode, YNode, LeafNode
from src.util import *


class NewTrapezoids:
    """Class for new trapezoids.

    It is used as a container for the new trapezoids that have been generated after adding a new segment to an existing
    trapezoidal map.

    Attributes:
        first (Optional[Trapezoid]): The trapezoid to the left of the segment.
        last (Optional[Trapezoid]): The trapezoid to the right of the segment.
        upper (List[Trapezoid]): The list of trapezoids above the segment.
        lower (List[Trapezoid]): The list of trapezoids below the segment.
    """

    def __init__(self, first: Optional[Trapezoid], last: Optional[Trapezoid],
                 upper: List[Trapezoid], lower: List[Trapezoid]):
        """Initializes a NewTrapezoids object.

        Args:
        first (Optional[Trapezoid]): The trapezoid to the left of the segment.
        last (Optional[Trapezoid]): The trapezoid to the right of the segment.
        upper (List[Trapezoid]): The list of trapezoids above the segment.
        lower (List[Trapezoid]): The list of trapezoids below the segment.
        """
        self.first = first
        self.last = last
        self.upper = upper
        self.lower = lower

    def __str__(self) -> str:
        """Returns the string representation of a NewTrapezoids object.
        """

        from itertools import groupby

        res = ""

        res += "\tFirst:\n"
        res += str(self.first) + "\n"

        res += "\tUpper:\n\t{\n"
        for delta in [x[0] for x in groupby(self.upper)]:
            res += str(delta)
        res += "\t}\n\n"

        res += "\tLower:\n\t{\n"
        for delta in [x[0] for x in groupby(self.lower)]:
            res += str(delta)
        res += "\t}\n\n"

        res += "\tLast:\n"
        res += str(self.last) + "\n"

        return res


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
            res += "\n" + str(trapezoid)

        res += "\nSize: " + str(len(self.trapezoids))

        return res

    def add_trapezoid(self, trapezoid: Trapezoid) -> None:
        """Adds a trapezoid to the trapezoidal map.

        Args:
            trapezoid (Trapezoid): The trapezoid to add.
        """

        if trapezoid is not None:
            self.trapezoids.add(trapezoid)  # TODO: Only keep valid trapezoids
            print("\t(+) Trapezoid " + get_id(trapezoid) + " added.")

    def add_trapezoids(self, new_ts: NewTrapezoids) -> None:
        """Adds multiple trapezoids to the trapezoidal map.

        Args:
            new_ts: The container of the new trapezoids.
        """

        self.add_trapezoid(new_ts.first)
        for delta in set(new_ts.upper):
            self.add_trapezoid(delta)
        for delta in set(new_ts.lower):
            self.add_trapezoid(delta)
        self.add_trapezoid(new_ts.last)

    def remove_trapezoid(self, trapezoid: Trapezoid) -> None:
        """Removes a trapezoid from the trapezoidal map.

        Args:
            trapezoid (Trapezoid): The trapezoid to remove.
        """

        self.trapezoids.discard(trapezoid)
        print("\t(-) Trapezoid " + get_id(trapezoid) + " removed.")

    def remove_trapezoids(self, old_ts: List[Trapezoid]) -> None:
        """Removes multiple trapezoids from the trapezoidal map.

        Args:
            old_ts: The list of the old trapezoids.
        """

        for delta in old_ts:
            self.remove_trapezoid(delta)

    def follow_segment(self, s: Segment) -> List[Trapezoid]:
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

        print("\n>>> Finding the intersected trapezoids...")

        # Initialize the list of trapezoids.
        deltas = []

        # Get the endpoints of the segment.
        p, q = s.p, s.q

        # Query the segment's left endpoint on the search structure.
        node = self.D.root.traverse(p)

        while not isinstance(node, LeafNode):
            # Move the query point to the right by an epsilon, in the direction of the segment.
            m = (q.y - p.y) / (q.x - p.x)
            epsilon = 0.0000001
            new_x = p.x + epsilon
            new_y = p.y + m * epsilon
            new_p = Point(new_x, new_y)

            print("The endpoint " + str(p) + " already exists. Retrying the query with " + str(new_p) + "...")

            # Restart the traversal from the current node.
            node = node.traverse(new_p)

        if isinstance(node, LeafNode):
            curr = node.trapezoid
        else:
            curr = None

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

        return deltas

    def update(self, s: Segment, old_ts: List[Trapezoid]) -> None:
        """Updates the trapezoidal map after some trapezoids have been intersected by the segment.

        The intersected trapezoids are removed and replaced with the new ones. The search structure is also updated.

        Args:
            s (Segment): The segment.
            old_ts (List[Trapezoids]): The list of intersected trapezoids.
        """

        print("\n>>> Updating the trapezoidal map...")

        # Check whether one or more trapezoids have been intersected.
        if len(old_ts) == 1:
            print("Single trapezoid detected.")

            # Get the single intersected trapezoid.
            old = old_ts[0]

            # Generate the new trapezoids.
            A = Trapezoid(old.top, old.bottom, old.leftp, s.p)  # Leftmost trapezoid
            B = Trapezoid(old.top, old.bottom, s.q, old.rightp)  # Rightmost trapezoid
            C = Trapezoid(old.top, s, s.p, s.q)  # Upper trapezoid
            D = Trapezoid(s, old.bottom, s.p, s.q)  # Lower trapezoid

            # Get the default neighbors.
            uln = old.uln
            lln = old.lln
            urn = old.urn
            lrn = old.lrn

            # Set the neighbors of each new trapezoid.
            if A.leftp != A.rightp:
                A.set_neighbors(uln, lln, C, D)
                uln = A
                lln = A
            else:
                A = None
            if B.leftp != B.rightp:
                B.set_neighbors(C, D, urn, lrn)
                urn = B
                lrn = B
            else:
                B = None
            C.set_neighbors(uln, None, urn, None)
            D.set_neighbors(None, lln, None, lrn)

            new_ts = NewTrapezoids(A, B, [C], [D])
        else:
            print("Multiple trapezoids detected.")

            # Split the intermediate intersected trapezoids into their upper and lower parts.
            print("Splitting the intermediate trapezoids...")
            upper_split, lower_split = split_trapezoids(s, old_ts)

            # Merge the upper and the lower parts where possible.
            print("Merging the upper parts...")
            upper = merge_trapezoids(upper_split)
            print("Merging the lower parts...")
            lower = merge_trapezoids(lower_split)

            # Get the default neighbors.
            uln = old_ts[0].uln
            lln = old_ts[0].lln
            urn = old_ts[-1].urn
            lrn = old_ts[-1].lrn

            # Check the existence of the leftmost and rightmost new trapezoids.
            first = Trapezoid(old_ts[0].top, old_ts[0].bottom, old_ts[0].leftp, s.p)
            last = Trapezoid(old_ts[-1].top, old_ts[-1].bottom, s.q, old_ts[-1].rightp)
            if first.leftp != first.rightp:
                first.set_neighbors(uln, lln, upper[0], lower[0])
                uln = first
                lln = first
            else:
                first = None
            if last.leftp != last.rightp:
                last.set_neighbors(upper[-1], lower[-1], urn, lrn)
                urn = last
                lrn = last
            else:
                last = None

            # Set the neighbors of each merged trapezoid.
            print("Updating the neighbors of the upper trapezoids...")
            update_neighbors(upper_split, upper, uln, urn, True)
            print("Updating the neighbors of the lower trapezoids...")
            update_neighbors(lower_split, lower, lln, lrn, False)

            new_ts = NewTrapezoids(first, last, upper, lower)

        print("\nIntersected trapezoids:")
        for delta in old_ts:
            print(get_id(delta))

        print("\nNew trapezoids:")
        print(new_ts)

        # Remove the old trapezoids and add the new ones.
        self.remove_trapezoids(old_ts)
        self.add_trapezoids(new_ts)

        # Update the search structure.
        self.D.update(s, old_ts, new_ts)


class SearchStructure:
    """Class for search structures.

    The search structure is a directed acyclic graph (DAG) used to query the location of points in trapezoids.
    All inner nodes have an out-degree of exactly 2 and can be X-nodes (endpoints) or Y-nodes (segments). Each leaf of
    the DAG represents a trapezoid.

    Attributes:
        root (Node): The root of the directed acyclic graph.
    """

    def __init__(self, R: Trapezoid) -> None:
        """Initializes a SearchStructure object.

        Args:
            R (Trapezoid): The bounding box rectangle.
        """

        print("Initializing the search structure...")

        # Create the root and add it to the set of nodes.
        self.root = R.leaf

    def __str__(self) -> str:
        """Returns the string representation of a SearchStructure object.
        """

        res = "root:" + str(self.root)

        return res

    def update(self, s: Segment, old_ts: List[Trapezoid], new_ts: NewTrapezoids) -> None:
        """Updates the search structure after some trapezoids have been intersected by the segment.

        The leaves of intersected trapezoids are removed and replaced with the ones of the new trapezoids, also adding
        some inner nodes and the necessary edges.

        Args:
            s (Segment): The segment.
            old_ts (List[Trapezoid]): The list of intersected trapezoids.
            new_ts (NewTrapezoids): The container of the new trapezoids.
        """

        print("\n>>> Updating the search structure...")

        x_nodes = set()
        y_nodes = set()

        # Check the number of intersected trapezoids.
        if len(old_ts) == 1:
            # Get the leaf of the old trapezoid.
            old = old_ts[0].leaf

            # Get the new trapezoids.
            A = new_ts.first
            B = new_ts.last
            C = new_ts.upper[0]
            D = new_ts.lower[0]

            # Create the inner nodes.
            np = XNode(s.p)
            ns = YNode(s)
            nq = XNode(s.q)
            sub_root = None

            # Add the leaves of the intermediate trapezoids.
            ns.set_left_child(C.leaf)
            ns.set_right_child(D.leaf)

            # Create the subtree depending from the existence of A and B.
            if A is not None and B is not None:
                nq.set_left_child(ns)
                nq.set_right_child(B.leaf)
                np.set_left_child(A.leaf)
                np.set_right_child(nq)
                sub_root = np
                y_nodes.add(np)
                y_nodes.add(nq)
            if A is not None and B is None:
                np.set_left_child(A.leaf)
                np.set_right_child(ns)
                sub_root = np
                y_nodes.add(np)
            if A is None and B is not None:
                nq.set_left_child(ns)
                nq.set_right_child(B.leaf)
                sub_root = nq
                y_nodes.add(nq)
            if A is None and B is None:
                sub_root = ns
                y_nodes.add(ns)

            if sub_root is not None:
                # Replace the old leaf with the new subtree where needed.
                if self.root == old:
                    self.root = sub_root
                else:
                    sub_root.replace_leaf(old)

        else:
            # Get the new trapezoids.
            first = new_ts.first
            last = new_ts.last
            upper = new_ts.upper
            lower = new_ts.lower

            # Create the Y-nodes.
            ns_list = []
            for i in range(len(old_ts)):
                ns = YNode(s)
                ns_list.append(ns)

                # Set the children of the Y-node.
                ns.set_left_child(upper[i].leaf)
                ns.set_right_child(lower[i].leaf)

            y_nodes = set(ns_list)

            # Replace the leftmost and rightmost leaves with X-nodes if needed.
            np = None
            nq = None
            if first is not None:
                np = XNode(s.p)
                np.set_left_child(first.leaf)
                np.set_right_child(ns_list[0])

                old_first = old_ts[0].leaf
                np.replace_leaf(old_first)
                x_nodes.add(np)
            if last is not None:
                nq = XNode(s.q)
                nq.set_left_child(ns_list[-1])
                nq.set_right_child(last.leaf)

                old_last = old_ts[-1].leaf
                nq.replace_leaf(old_last)
                x_nodes.add(nq)

            # Replace each remaining leaf with a Y-node.
            for i in range(len(old_ts)):
                ns = ns_list[i]
                old = old_ts[i].leaf

                # Replace the leaf of the old trapezoid.
                ns.replace_leaf(old)

        print("X-nodes:")
        for x_node in x_nodes:
            print(x_node)

        print("Y-nodes:")
        for y_node in y_nodes:
            print(y_node)

    def query(self, q: Point) -> Optional[Trapezoid]:
        """Queries a point in the search structure.

        Querying a point consists in a recursive traversal of the search structure's DAG, starting from the root.
        If the traversal reaches a leaf, the corresponding trapezoid is returned. Otherwise, the query has failed.

        Args:
            q (Point): The query point.

        Returns:
            Optional[Trapezoid]: The trapezoid that contains the query point.
        """

        print("Querying point " + str(q) + "...")

        # Start from the root of the search structure.
        node = self.root

        # Traverse the search structure.
        res = node.traverse(q)

        # Check whether a leaf node has been reached.
        if isinstance(res, LeafNode):
            face = res.trapezoid
        else:
            face = None
            print("The query point is not valid.")

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
        print(R)

        # Initialize the trapezoidal map.
        self.T = TrapezoidalMap(R)

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
            if p.y > max_y:
                max_y = p.y
            if q.y < min_y:
                min_y = q.y
            if q.y > max_y:
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
        random.shuffle(segments)

        # Iteratively build the trapezoidal map.
        for i in range(len(segments)):
            print("\n" + 80 * "~")
            print("\tITERATION " + str(i) + ":\t" + str(segments[i]) + "\n")

            # Find the intersected trapezoids.
            deltas = self.T.follow_segment(segments[i])

            # Update the trapezoidal map and the search structure.
            self.T.update(segments[i], deltas)

        print("\n" + 80 * "~")
        print("Construction completed.")
