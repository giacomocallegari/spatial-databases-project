from src.geometry import Point, Segment
from src.structures import Subdivision


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
    print(str(S))

    """
    # Build the trapezoidal map and the search structure.
    print("\n*** DATA STRUCTURES ***")
    S.trapezoidal_map()
    """

    """
    # Query a sample point.
    print("\n*** SAMPLE QUERY ***")
    query_point = Point(2, 4)
    face = S.D.query(query_point)
    """


if __name__ == "__main__":
    main()
