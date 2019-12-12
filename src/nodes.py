from typing import *

from src.geometry import Point, Segment, Trapezoid


class Node:
    """Class for the nodes of the search structure.

    Attributes:
        left_child (Node): The left child.
        right_child (Node): The right child.
    """

    def __init__(self) -> None:
        """Initializes Node.
        """

        self.left_child = None
        self.right_child = None

    def __str__(self) -> str:
        """Returns the string representation of a Node object.
        """

        res = "\n\n"
        res += "left_child = " + self.left_child
        res += "right_child = " + self.right_child

        return res

    def set_left_child(self, child: Optional["Node"]) -> None:
        """Sets the left child of the current node.

        Args:
            child (Optional[Node]): The left child.
        """

        self.left_child = child

    def set_right_child(self, child: Optional["Node"]) -> None:
        """Sets the right child of the current node.

        Args:
            child (Optional[Node]): The right child.
        """

        self.right_child = child

    def traverse(self, q: Point) -> Optional[Trapezoid]:
        """Recursively traverses the search structure until a leaf is reached.

        In the search structure, each leaf represents a trapezoid of the refined subdivision. The search starts from the
        root and, by evaluating the inner nodes, a path to a leaf is obtained.
        X-nodes represent endpoints of the subdivision: the query point is either to the left or to the right.
        Y-nodes represent segments of the subdivision: the query point is either above or below.
        The traversal is performed recursively, exploiting the tree-like structure of the DAG.

        Args:
            q (Point): The query point.
        """

        # print(str(node))

        # If the node is a leaf, it represents a trapezoid.
        if isinstance(self, LeafNode):
            return self.trapezoid
        else:
            # If the node is an X-node, it represents an endpoint.
            if isinstance(self, XNode):
                nnext = self.left_child if not q.lies_right(self.point) else self.right_child
            # If the node is a Y-node, it represents as segment.
            elif isinstance(self, YNode):
                nnext = self.left_child if not q.lies_above(self.segment) else self.right_child
            else:
                print("Error: Wrong node type.")
                return

            # Recursively traverse the DAG.
            return nnext.traverse(q)


class XNode(Node):
    """Class for X-nodes of the search structure.

    Attributes:
        point (Point): The referenced endpoint.
    """

    def __init__(self, point: Point) -> None:
        """Initializes XNode with the referenced endpoint.

        Args:
            point: The referenced endpoint.
        """

        super().__init__()
        self.point = point


class YNode(Node):
    """Class for Y-nodes of the search structure.

    Attributes:
        segment (Segment): The referenced segment.
    """

    def __init__(self, segment: Segment) -> None:
        """Initializes YNode with the referenced segment.

        Args:
            segment: The referenced segment.
        """

        super().__init__()
        self.segment = segment


class LeafNode(Node):
    """Class for leaf nodes of the search structure.

    Attributes:
        trapezoid (Trapezoid): The referenced trapezoid.
    """

    def __init__(self, trapezoid: Trapezoid) -> None:
        """Initializes LeafNode with the referenced trapezoid.

        Args:
            trapezoid: The referenced trapezoid.
        """

        super().__init__()
        self.trapezoid = trapezoid
