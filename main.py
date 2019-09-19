from geometry import Point, Segment, Subdivision


def main():
    """Main function."""

    # Create a sample subdivision.
    p1 = Point(0, 0)
    p2 = Point(0, 1)
    p3 = Point(1, 0)
    s1 = Segment(p1, p2)
    s2 = Segment(p2, p3)
    sub = Subdivision([s1, s2])

    print(sub)


if __name__ == "__main__":
    main()
