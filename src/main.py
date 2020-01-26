from src.geometry import Point, Segment
from src.structures import Subdivision


def main():
    """Main function.

    After providing a sample subdivision, its trapezoidal map and search structure are built.
    Then, points can be queried to find which faces contain them.
    """

    example = 2  # Number of the example

    # Create a sample subdivision.
    print("\n\n*** INITIALIZATION ***")

    segments = set()

    if example == 1:
        p1 = Point(2, 4)
        q1 = Point(9, 6)
        p2 = Point(6, 3)
        q2 = Point(12, 2)
        s1 = Segment(p1, q1)
        s2 = Segment(p2, q2)
        segments = {s1, s2}
    elif example == 2:
        p1 = Point(10, 8)
        p2 = Point(2, 4)
        p3 = Point(6, 2)
        p4 = Point(20, 4)
        p5 = Point(12, 10)
        p6 = Point(16, 6)
        s1 = Segment(p1, p2)
        s2 = Segment(p2, p3)
        s3 = Segment(p3, p4)
        s4 = Segment(p4, p5)
        s5 = Segment(p2, p6)
        segments = {s1, s2, s3, s4, s5}

    S = Subdivision(segments)

    # Build the trapezoidal map and the search structure.
    print("\n\n*** CONSTRUCTION ***")

    S.trapezoidal_map()

    # Query a sample point.
    print("\n\n*** QUERY ***")

    query_point = Point(4, 2)
    face = S.T.D.query(query_point)

    print("\nPoint " + str(query_point) + " is located here:\n" + str(face))


if __name__ == "__main__":
    main()
