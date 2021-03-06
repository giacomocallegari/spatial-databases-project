from typing import *

from src.geometry import Point, Segment, Trapezoid
from src.util import *


class Node:
    """Class for the nodes of a search structure.

    Attributes:
        parents (Set[Node]): The parents.
        left_child (Optional[Node]): The left child.
        right_child (Optional[Node]): The right child.
    """

    def __init__(self) -> None:
        """Initializes Node.
        """

        self.parents = set()
        self.left_child = None
        self.right_child = None

    def __str__(self) -> str:
        """Returns the string representation of a Node object.
        """

        res = ""
        res += "\tNode ID: " + get_id(self) + "\n"
        res += "\tleft_child:\t" + get_id(self.left_child) + "\n"
        res += "\tright_child:\t" + get_id(self.right_child) + "\n"

        return res

    def add_parent(self, parent: "Node") -> None:
        """Adds a new parent for the current node.

        Args:
            parent (Node): The new parent.
        """

        self.parents.add(parent)

    def remove_parents(self):
        """Removes all parents from the current node.
        """

        # Clear the parents.
        self.parents.clear()

    def set_left_child(self, child: Optional["Node"]) -> None:
        """Sets the left child of the current node.

        Args:
            child (Optional[Node]): The left child.
        """

        self.left_child = child

        if child is not None:
            # Add the current node as a parent of the child.
            child.add_parent(self)

    def set_right_child(self, child: Optional["Node"]) -> None:
        """Sets the right child of the current node.

        Args:
            child (Optional[Node]): The right child.
        """

        self.right_child = child

        if child is not None:
            # Add the current node as a parent of the child.
            child.add_parent(self)

    def replace_leaf(self, old: "Node") -> None:
        """Replaces an existing leaf by updating the children of all its parents.

        Args:
            old (Node): The leaf to replace.
        """

        # Iterate over all the parents of the old leaf.
        for parent in old.parents:
            if old == parent.left_child:
                # Become the new left child.
                parent.set_left_child(self)
            if old == parent.right_child:  #
                # Become the new right child.
                parent.set_right_child(self)

        # old.remove_parents()

    def traverse(self, q: Point) -> Optional["Node"]:
        """Recursively traverses the search structure until a leaf, or an X-node if the point is already present.

        In the search structure, each leaf represents a trapezoid of the refined subdivision. The search starts from the
        root and, by evaluating the inner nodes, a path to a leaf is obtained.
        X-nodes represent endpoints of the subdivision: the query point is either to the left or to the right.
        Y-nodes represent segments of the subdivision: the query point is either above or below.
        The traversal is performed recursively, exploiting the tree-like structure of the DAG.

        Args:
            q (Point): The query point.

        Returns:
            Optional[Node]: The resulting node.
        """

        # If the node is a leaf, it represents a trapezoid.
        if isinstance(self, LeafNode):
            print("Trapezoid ID: " + get_id(self.trapezoid))
            return self
        else:
            # If the node is an X-node, it represents an endpoint.
            if isinstance(self, XNode):
                if q.x == self.point.x and q.y == self.point.y:
                    # Stop the traversal at the current X-node.
                    return self
                else:
                    if q.lies_left(self.point):
                        print("<-\t" + str(self.point))
                        nnext = self.left_child
                    else:
                        print("->\t" + str(self.point))
                        nnext = self.right_child

            # If the node is a Y-node, it represents as segment.
            elif isinstance(self, YNode):
                if q.x == self.segment.p.x and q.y == self.segment.p.y:
                    # Stop the traversal at the current Y-node.
                    return self
                else:
                    if q.lies_above(self.segment):
                        print("/\\\t" + str(self.segment))
                        nnext = self.left_child
                    else:
                        print("\\/\t" + str(self.segment))
                        nnext = self.right_child

            else:
                print("Error: Wrong node type.")
                return

            # Recursively traverse the DAG.
            return nnext.traverse(q)


class XNode(Node):
    """Class for X-nodes of a search structure.

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

    def __str__(self) -> str:
        """Returns the string representation of a XNode object.
        """

        res = super().__str__()
        res += "\tPoint: " + str(self.point) + "\n"

        return res


class YNode(Node):
    """Class for Y-nodes of a search structure.

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

    def __str__(self) -> str:
        """Returns the string representation of a YNode object.
        """

        res = super().__str__()
        res += "\tSegment: " + str(self.segment) + "\n"

        return res


class LeafNode(Node):
    """Class for leaf nodes of a search structure.

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
