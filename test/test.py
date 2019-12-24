from src.geometry import Point, Segment, Trapezoid
from src.util import merge_trapezoids


def test_merge_trapezoids():
    p1 = Point(1, 1)
    q1 = Point(18, 1)
    p2 = Point(6, 5)
    q2 = Point(10, 6)
    p3 = Point(13, 3)
    q3 = Point(14, 4)
    p4 = Point(14, 4)
    q4 = Point(17, 3)
    p = Point(2, 4)
    q = Point(13, 3)

    s1 = Segment(p1, q1)
    s2 = Segment(p2, q2)
    s3 = Segment(p3, q3)
    s4 = Segment(p4, q4)
    s = Segment(p, q)

    A = Trapezoid(s, s1, p, p2)
    B = Trapezoid(s, s1, p2, q2)
    C = Trapezoid(s, s1, q2, q)
    D = Trapezoid(s3, s1, p3, q3)
    E = Trapezoid(s4, s1, p4, q4)

    merged = merge_trapezoids([A, B, C, D, E])

    for delta in merged:
        print(delta)


test_merge_trapezoids()
