from src.geometry import *
from enum import Enum
from typing import *


class Trapezoid:
    """Class for trapezoids.

    Attributes:
        top (Segment): The top non-vertical side.
        bottom (Segment): The bottom non-vertical side.
        leftp (Point): The left generator endpoint.
        rightp (Point): The right generator endpoint.
        uln (Optional[Trapezoid]): The upper left neighbor.
        lln (Optional[Trapezoid]): The lower left neighbor.
        urn (Optional[Trapezoid]): The upper right neighbor.
        lrn (Optional[Trapezoid]): The lower right neighbor.
    """

    def __init__(self, top: Segment, bottom: Segment, leftp: Point, rightp: Point) -> None:
        """Initializes a Trapezoid object.

        Args:
            top (Segment): The top non-vertical side.
            bottom (Segment): The bottom non-vertical side.
            leftp (Point): The left generator endpoint.
            rightp (Point): The right generator endpoint.
        """

        self.top = top
        self.bottom = bottom
        self.leftp = leftp
        self.rightp = rightp
        self.uln = None
        self.lln = None
        self.urn = None
        self.lrn = None

    def __str__(self) -> str:
        """Returns the string representation of a Trapezoid object.
        """

        res = ""
        res += "top:\t" + str(self.top) + "\n"
        res += "bottom:\t" + str(self.bottom) + "\n"
        res += "leftp = " + str(self.leftp) + "\trightp = " + str(self.rightp) + "\n"
        res += "uln = " + str(self.uln) + "\turn = " + str(self.urn) + "\n"
        res += "lln = " + str(self.lln) + "\tlrn = " + str(self.lrn) + "\n"

        return res

    def set_neighbors(self, uln: Optional["Trapezoid"], lln: Optional["Trapezoid"],
                      urn: Optional["Trapezoid"], lrn: Optional["Trapezoid"]) -> None:
        self.uln = uln
        self.lln = lln
        self.urn = urn
        self.lrn = lrn


class TrapezoidalMap:
    """Class for trapezoidal maps.

    A trapezoidal map is a refinement of a subdivision, obtained by drawing for each segment endpoint vertical
    extensions that stop at the first non-vertical line.
    Every element of the map is a trapezoid, or a triangle in the degenerate case. The structure is therefore
    represented as a set of Trapezoid objects.
    The whole map is enclosed in a bounding box, which is a rectangle.

    Attributes:
        trapezoids (Set[Trapezoids]): The set of trapezoids.
    """

    def __init__(self, R: Trapezoid) -> None:
        """Initializes a TrapezoidalMap object.

        Args:
            R (Trapezoid): The bounding box rectangle.
        """

        print("Initializing the trapezoidal map...")

        self.trapezoids = set()

        # Add the initial trapezoid, which is the bounding box.
        self.add_trapezoid(R)

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

    def merge(self, parts: List[Trapezoid]) -> List[Trapezoid]:
        """Merges the adjacent trapezoids that share the same non-vertical sides.

        Args:
            parts (List[Trapezoid]): The list of parts of trapezoids.

        Returns:
            List[Trapezoid]: The list of merged trapezoids.
        """

        res = []

        # Merge the parts.
        for i in range(1, len(parts)):
            pred = parts[i - 1]
            curr = parts[i]

            # Check if adjacent parts share the same non-vertical sides.
            if curr.top == pred.top and curr.bottom == pred.bottom:
                parts[i] = Trapezoid(pred.top, pred.bottom, pred.leftp, curr.rightp)
            else:
                res.append(pred)

        return res

    def update(self, s: Segment, delta: List[Trapezoid]) -> None:  # TODO
        """Updates the trapezoidal map after some trapezoids have been intersected by the segment.

        The intersected trapezoids are removed and replaced with the new ones.

        Args:
            s (Segment): The segment.
            delta (List[Trapezoids]): The list of intersected trapezoids.
        """

        # Remove the intersected trapezoids.
        # for trapezoid in delta:
        #     self.remove_trapezoid(trapezoid)

        # Check whether one or more trapezoids have been intersected.
        if len(delta) == 1:
            # Get the single intersected trapezoid.
            old = delta[0]

            # Generate the new trapezoids.
            A = Trapezoid(old.top, old.bottom, old.leftp, s.p1)
            B = Trapezoid(old.top, old.bottom, s.p2, old.rightp)
            C = Trapezoid(old.top, s, s.p1, s.p2)
            D = Trapezoid(s, old.top, s.p1, s.p2)

            # Set the neighbors of the new trapezoids.
            A.set_neighbors(old.uln, old.lln, C, D)
            B.set_neighbors(C, D, old.urn, old.lrn)
            C.set_neighbors(A, None, B, None)
            D.set_neighbors(None, old.lln, None, old.lrn)

            # Add the new trapezoids and remove the old one.
            self.remove_trapezoid(old)
            self.trapezoids = self.trapezoids.union({A, B, C, D})
        else:
            # TODO: Degenerate case
            # Create the leftmost and rightmost new trapezoids.
            first = Trapezoid(delta[0].top, delta[0].bottom, delta[0].leftp, s.p1)
            last = Trapezoid(delta[-1].top, delta[-1].bottom, s.p2, delta[-1].rightp)

            # Create the lists for the upper and the lower parts of the intersected trapezoids.
            upper = []
            lower = []

            # Split each intersected trapezoid into its upper and lower parts.
            upper.append(Trapezoid(first.top, s, s.p1, first.rightp))
            lower.append(Trapezoid(s, first.bottom, s.p1, first.rightp))
            for i in range(1, len(delta) - 1):
                curr = delta[i]
                upper.append(Trapezoid(curr.top, s, curr.leftp, curr.rightp))
                lower.append(Trapezoid(s, curr.bottom, curr.leftp, curr.rightp))
            upper.append(Trapezoid(last.top, s, last.leftp, s.p2))
            lower.append(Trapezoid(s, last.bottom, last.leftp, s.p2))

            # Merge the upper and the lower parts where possible.
            upper = self.merge(upper)
            lower = self.merge(lower)

            # Set the neighbors of each trapezoid.
            first.set_neighbors(delta[0].uln, delta[0].lln, upper[0], lower[0])
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
            last.set_neighbors(upper[-1], lower[-1], delta[-1].urn, delta[-1].lrn)

            # Add the new trapezoids to the map.
            self.add_trapezoid(first)
            for trapezoid in upper:
                self.add_trapezoid(trapezoid)
            for trapezoid in lower:
                self.add_trapezoid(trapezoid)
            self.add_trapezoid(last)


class NodeType(Enum):
    """Enumeration for the types of node.
    """

    LEAF = 0
    X_NODE = 1
    Y_NODE = 2


class Node:
    """Class for the nodes of the search structure.

    Attributes:
        ntype (NodeType): The type of the node.
        item (Union[Point, Segment, Trapezoid]): The referenced item.
        left (Node): The left child.
        right (Node): The right child.
    """

    def __init__(self, ntype: NodeType, item: Union[Point, Segment, Trapezoid]) -> None:
        """Initializes Node with the type and the referenced item.

        Args:
            ntype (str): The type of the node.
            item (Union[Point, Segment, Trapezoid]): The referenced item.
        """

        self.ntype = ntype
        self.item = item
        self.left = None
        self.right = None

    def __str__(self) -> str:
        """Returns the string representation of a Node object.
        """

        res = "\n\n"

        res += "ntype = " + str(self.ntype) + "\n"
        res += "item = " + str(self.item) + "\n"
        # res += "left = " + self.left.item
        # res += "right = " + self.right.item

        return res

    def set_left_child(self, child: Optional["Node"]) -> None:
        """Sets the left child of the current node.

        Args:
            child (Optional[Node]): The left child.
        """

        self.left = child

    def set_right_child(self, child: Optional["Node"]) -> None:
        """Sets the right child of the current node.

        Args:
            child (Optional[Node]): The right child.
        """

        self.right = child


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
        self.root = Node(NodeType.LEAF, R)
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

    def update(self, T: TrapezoidalMap, s: Segment, delta: List[Trapezoid]) -> None:  # TODO
        """Updates the search structure after some trapezoids have been intersected by the segment.

        The leaves of intersected trapezoids are removed and replaced with the ones of the new trapezoids, also adding
        some inner nodes.

        Args:
            T (TrapezoidalMap): The corresponding trapezoidal map.
            s (Segment): The segment.
            delta (List[Trapezoid]): The list of intersected trapezoids.
        """

        # Remove the leaves of the intersected trapezoids.
        for trapezoid in delta:
            leaf = self.nodes.get(id(trapezoid))
            self.remove_node(leaf)

        # Check whether one or more trapezoids have been intersected.
        if len(delta) == 1:
            print("Single trapezoid")

            parent = self.nodes.get(id(delta[0]))  # TODO

            # Get the new trapezoids.
            A, B, C, D = T.trapezoids  # TODO

            # Add the leaves of the new trapezoids.
            nA = Node(NodeType.LEAF, A)
            nB = Node(NodeType.LEAF, B)
            nC = Node(NodeType.LEAF, C)
            nD = Node(NodeType.LEAF, D)
            self.add_node(nA)
            self.add_node(nB)
            self.add_node(nC)
            self.add_node(nD)

            # Add the inner nodes.
            np1 = Node(NodeType.X_NODE, s.p1)
            np2 = Node(NodeType.X_NODE, s.p2)
            ns = Node(NodeType.Y_NODE, s)
            self.add_node(np1)
            self.add_node(np2)
            self.add_node(ns)

            # Add the edges.
            parent.set_left_child()
            parent.set_right_child()
            np1.set_left_child(nA)
            np1.set_right_child(np2)
            np2.set_left_child(ns)
            np2.set_right_child(nB)
            ns.set_left_child(nC)
            ns.set_right_child(nD)

        else:  # TODO
            print("Multiple trapezoids")
