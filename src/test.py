from src.geometry import Point, Segment, Trapezoid
from src.nodes import XNode, YNode, LeafNode


# ---GEOMETRY----

# Points
p1 = Point(1, 3)
q1 = Point(5, 4)
p2 = Point(3, 2)
q2 = Point(6, 1)
ll = Point(0, 0)
lr = Point(7, 0)
ul = Point(0, 6)
ur = Point(7, 6)

# Segments
s1 = Segment(p1, q1)
s2 = Segment(p2, q2)
ls = Segment(ll, lr)
us = Segment(ul, ur)

# Trapezoids
A = Trapezoid(us, ls, ll, p1)
B = Trapezoid(us, s1, p1, q1)
C = Trapezoid(s1, ls, p1, p2)
D = Trapezoid(s1, s2, p2, q1)
E = Trapezoid(us, s2, q1, q2)
F = Trapezoid(s2, ls, p2, q2)
G = Trapezoid(us, ls, q2, lr)


# ----GRAPH----

# Nodes
n0 = XNode(p1)
n1 = LeafNode(A)
n2 = XNode(q1)
n3 = YNode(s1)
n4 = LeafNode(B)
n5 = XNode(p2)
n6 = LeafNode(C)
n7 = YNode(s2)
n8 = LeafNode(D)
n9 = LeafNode(F)
n10 = XNode(q2)
n11 = YNode(s2)
n12 = LeafNode(E)
n13 = LeafNode(G)

# Children
n0.set_left_child(n1)
n0.set_right_child(n2)
n2.set_left_child(n3)
n2.set_right_child(n10)
n3.set_left_child(n4)
n3.set_right_child(n5)
n5.set_left_child(n6)
n5.set_right_child(n7)
n7.set_left_child(n8)
n7.set_right_child(n9)
n10.set_left_child(n11)
n10.set_right_child(n13)
n11.set_left_child(n12)
n11.set_right_child(n9)


# ----QUERY----

# Query a point on the DAG.
query_point = Point(4, 3)
face = n0.traverse(query_point)

print(face)
