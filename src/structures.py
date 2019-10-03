import networkx as nx

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

    def update(self, s: Segment, delta: List[Trapezoid]) -> None:  # TODO
        """Updates the trapezoidal map after some trapezoids have been intersected by the segment.

        The intersected trapezoids are removed and replaced with the new ones.

        Args:
            s (Segment): The segment.
            delta (List[Trapezoids]): The list of intersected trapezoids.
        """

        # Remove the intersected trapezoids.
        for trapezoid in delta:
            self.remove_trapezoid(trapezoid)

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

            # Add the new trapezoids.
            self.trapezoids.union({A, B, C, D})
        else:  # TODO
            print("Multiple trapezoids")


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

    def set_left_child(self, child: "Node") -> None:
        """Sets the left child of the current node.

        Args:
            child (Node): The left child.
        """

        self.left = child

    def set_right_child(self, child: "Node") -> None:
        """Sets the right child of the current node.

        Args:
            child (Node): The right child.
        """

        self.right = child


class SearchStructure:
    """Class for the search structure.

    The search structure is a directed acyclic graph (DAG) used to query the location of points in trapezoids.
    All inner nodes have an out-degree of exactly 2 and can be X-nodes (endpoints) or Y-nodes (segments). Each leaf of
    the DAG represents a trapezoid.

    Attributes:
        root (dict): The root of the directed acyclic graph.
    """

    def __init__(self, R: Trapezoid) -> None:
        """Initializes a SearchStructure object.

        Args:
            R (Trapezoid): The bounding box rectangle.
        """

        print("Initializing the search structure...")

        self.root = Node(NodeType.LEAF, R)

    def __str__(self) -> str:
        """Returns the string representation of a SearchStructure object.
        """

        res = "root:" + str(self.root)

        return res




class SearchStructureOld:
    """Class for the search structure.

    The search structure is a directed acyclic graph (DAG) used to query the location of points in trapezoids.
    Each leaf of the DAG represents a trapezoid, while inner nodes can be X-nodes (endpoints) or Y-nodes (segments).

    Attributes:
        dag (nx.DiGraph): The directed acyclic graph of the search structure.
    """

    def __init__(self, R: Trapezoid) -> None:
        """Initializes SearchStructure.
        """

        print("Initializing the search structure...")

        self.dag = nx.DiGraph()
        self.dag.add_node("R", type="leaf", item=R)

    def __str__(self) -> str:
        """Returns the string representation of a SearchStructure object.
        """

        res = str(nx.to_pandas_adjacency(self.dag, dtype=int))

        return res

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
            leaf = self.dag.nodes.get(id(trapezoid))
            self.dag.remove_node(leaf)

        # Check whether one or more trapezoids have been intersected.
        if len(delta) == 1:
            print("Single trapezoid")

            parent = self.dag.nodes.get(id(delta[0]))

            # Get the new trapezoids.
            A, B, C, D = T.trapezoids  # TODO

            # Add the leaves of the new trapezoids.
            self.dag.add_node(A, type="leaf")
            self.dag.add_node(B, type="leaf")
            self.dag.add_node(C, type="leaf")
            self.dag.add_node(D, type="leaf")

            # Add the inner nodes.
            self.dag.add_node(id(s.p1), type="x_node")
            self.dag.add_node(id(s.p2), type="x_node")
            self.dag.add_node(id(s), type="y_node")

            # Add the edges.
            self.dag.add_edge(parent, id(s.p1))
            self.dag.add_edge(id(s.p1), id(A))
            self.dag.add_edge(id(s.p1), id(s.p2))
            self.dag.add_edge(id(s.p2), id(s))
            self.dag.add_edge(id(s.p2), id(B))
            self.dag.add_edge(id(s), id(C))
            self.dag.add_edge(id(s), id(D))

        else:  # TODO
            print("Multiple trapezoids")


