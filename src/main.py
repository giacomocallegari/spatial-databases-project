import random
import networkx as nx
from src.geometry import Point, Segment, Subdivision
from src.structures import *
from typing import *


def traverse(q: Point, node: Node) -> Optional[Trapezoid]:  # TODO
    """Recursively traverses the search structure until a leaf.

    In the search structure, each leaf represents a trapezoid of the refined subdivision. The search starts from the
    root and, by evaluating the inner nodes, a path to a leaf is obtained.
    X-nodes represent endpoints of the subdivision: the query point is either to the left or to the right.
    Y-nodes represent segments of the subdivision: the query point is either above or below.
    The traversal is performed recursively, exploiting the tree-like structure of the DAG.

    Args:
        q (Point): The query point.
        node (Node): The current node of the DAG.
    """

    ntype = node.ntype
    item = node.item
    # print(str(node))

    # If the node is a leaf, it represents a trapezoid.
    if ntype == NodeType.LEAF:
        print("leaf")
        return item
    else:
        # If the node is an X-node, it represents an endpoint.
        if ntype == NodeType.X_NODE:
            print("x-node")
            nnext = node.left if not q.lies_right(item) else node.right
        # If the node is a Y-node, it represents as segment.
        elif ntype == NodeType.Y_NODE:
            print("y-node")
            nnext = node.left if not q.lies_above(item) else node.right
        else:
            print("Error: Wrong node type.")
            return

        # Recursively traverse the DAG.
        return traverse(q, nnext)


def query(q: Point, D: SearchStructure) -> Optional[Trapezoid]:  # TODO
    """Queries a point in the search structure.

    Querying a point consists in a recursive traversal of the search structure's DAG, from the root to a leaf.
    Once the trapezoid has been obtained, the corresponding face of the original subdivision can be found.

    Args:
        q (Point): The query point.
        D (SearchStructure): The search structure.

    Returns:
        The trapezoid that contains the query point.
    """

    # Start from the root of the search structure.
    node = D.root

    # Traverse the search structure until a leaf is reached.
    face = traverse(q, node)
    print(face)

    return face


def bounding_box(subdivision: Subdivision) -> Trapezoid:
    """Creates a bounding box for the subdivision.

    The bounding box is a rectangle that contains the whole subdivision, producing a bounded area where a trapezoidal
    map refinement can be applied.
    The extreme X and Y coordinates of the subdivision are obtained and, after applying a fixed margin of 1 to all
    sides, the rectangle is built.

    Args:
        subdivision (Subdivision): The original subdivision.

    Returns:
        Trapezoid: The bounding box rectangle, a particular case of trapezoid.
    """

    print("Building the bounding box...")

    # Get the extreme coordinates of the subdivision and add a margin of 1 to each side.
    x1 = subdivision.min_x - 1
    x2 = subdivision.max_x + 1
    y1 = subdivision.min_y - 1
    y2 = subdivision.max_y + 1

    # Set the corners of the rectangle.
    ll = Point(x1, y1)
    lr = Point(x2, y1)
    ul = Point(x1, y2)
    ur = Point(x2, y2)

    # Create and return the bounding box.
    return Trapezoid(Segment(ul, ur), Segment(ll, lr), ll, lr)


def follow_segment(T: TrapezoidalMap, D: SearchStructure, s: Segment) -> List[Trapezoid]:  # TODO
    """Finds the trapezoids that a segment intersects in a trapezoidal map.

    The search starts from the leftmost intersected trapezoid, obtained by querying the leftmost segment endpoint on the
    current trapezoidal map. Then, iteratively, the right neighbor of each intersected trapezoid is found until the
    rightmost endpoint is reached.
    The result is the list of intersected trapezoids, ordered from left to right.

    Args:
        T (TrapezoidalMap): The trapezoidal map.
        D (SearchStructure): The search structure.
        s (Segment): The segment.

    Returns:
        List[Trapezoid]: The list of intersected trapezoids.
    """

    # Initialize the list of trapezoids.
    delta = list()

    # Get the endpoints of the segment.
    p, q = s.p1, s.p2

    # Find the first intersected trapezoid.
    delta.append(query(p, D))  # TODO

    # Iteratively find the next intersected trapezoids.
    j = 0
    while q.lies_right(delta[j].rightp):
        if delta[j].rightp.lies_above(s):
            delta[j + 1] = delta[j].lrn
        else:
            delta[j + 1] = delta[j].urn

        j += 1

    return delta


def trapezoidal_map(S: Subdivision) -> (TrapezoidalMap, SearchStructure):  # TODO
    """Creates the trapezoidal map and the search structure from the subdivision.

    The trapezoidal map is a refinement of the original subdivision. It is completed by a search structure, which is a
    DAG representing the trapezoids as leaves.
    These structures can be used together to query which trapezoid contains a given point.

    Args:
        S (Subdivision): The original subdivision.

    Returns:
        (TrapezoidalMap, SearchStructure): The trapezoidal map and the search structure.
    """

    # Create the bounding box.
    R = bounding_box(S)
    # print(str(R))

    # Initialize the trapezoidal map and the search structure.
    T = TrapezoidalMap(R)
    # print(str(T))
    D = SearchStructure(R)
    # print(str(D))

    # Shuffle the segments of the subdivision.
    segments = S.segments
    random.shuffle(segments)

    # Iteratively build the structures.
    for i in range(len(segments)):
        # Find the intersected trapezoids.
        delta = follow_segment(T, D, segments[i])

        """
        # Update the trapezoidal map.
        T.update(segments[i], delta)

        # Update the search structure.
        D.update(T, segments[i], delta)
        """

    return T, D


def main():
    """Main function.

    After providing a sample subdivision, its trapezoidal map and search structure are built.
    Then, points can be queried to find which faces contain them.
    """

    # Create a sample subdivision.
    print("\n*** SAMPLE SUBDIVISION ***")
    p1 = Point(1, 3)
    q1 = Point(5, 4)
    p2 = Point(3, 2)
    q2 = Point(6, 1)
    s1 = Segment(p1, q1)
    s2 = Segment(p2, q2)
    S = Subdivision([s1, s2])
    # print(str(S))

    # Build the trapezoidal map and the search structure.
    print("\n*** DATA STRUCTURES ***")
    T, D = trapezoidal_map(S)

    """
    # Query a sample point.
    print("\n*** SAMPLE QUERY ***")
    q = Point(2, 4)
    face = query(q, D)
    """


if __name__ == "__main__":
    main()
