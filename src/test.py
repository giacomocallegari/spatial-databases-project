from src.main import traverse
from src.geometry import Point, Segment
from src.structures import Trapezoid, NodeType, Node


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
n0 = Node(NodeType.X_NODE, p1)
n1 = Node(NodeType.LEAF, A)
n2 = Node(NodeType.X_NODE, q1)
n3 = Node(NodeType.Y_NODE, s1)
n4 = Node(NodeType.LEAF, B)
n5 = Node(NodeType.X_NODE, p2)
n6 = Node(NodeType.LEAF, C)
n7 = Node(NodeType.Y_NODE, s2)
n8 = Node(NodeType.LEAF, D)
n9 = Node(NodeType.LEAF, F)
n10 = Node(NodeType.X_NODE, q2)
n11 = Node(NodeType.Y_NODE, s2)
n12 = Node(NodeType.LEAF, E)
n13 = Node(NodeType.LEAF, G)

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
q = Point(4, 3)
face = traverse(q, n0)

print(face)


"""
# DAG
dag = nx.DiGraph()

# Nodes
dag.add_node("0", label="p1", type="x_node", item=p1)
dag.add_node("1", label="A", type="leaf", item=A)
dag.add_node("2", label="q1", type="x_node", item=q1)
dag.add_node("3", label="s1", type="y_node", item=s1)
dag.add_node("4", label="B", type="leaf", item=B)
dag.add_node("5", label="p2", type="x_node", item=p2)
dag.add_node("6", label="C", type="leaf", item=C)
dag.add_node("7", label="s2", type="y_node", item=s2)
dag.add_node("8", label="D", type="leaf", item=D)
dag.add_node("9", label="F", type="leaf", item=F)
dag.add_node("10", label="q2", type="x_node", item=q2)
dag.add_node("11", label="s2", type="y_node", item=s2)
dag.add_node("12", label="E", type="leaf", item=E)
dag.add_node("13", label="G", type="leaf", item=G)

# Edges
dag.add_edge("0", "1", child="left")
dag.add_edge("0", "2", child="right")
dag.add_edge("2", "3", child="left")
dag.add_edge("2", "10", child="right")
dag.add_edge("3", "4", child="left")
dag.add_edge("3", "5", child="right")
dag.add_edge("5", "6", child="left")
dag.add_edge("5", "7", child="right")
dag.add_edge("7", "8", child="left")
dag.add_edge("7", "9", child="right")
dag.add_edge("10", "11", child="left")
dag.add_edge("10", "13", child="right")
dag.add_edge("11", "12", child="left")
dag.add_edge("11", "9", child="right")

# print(nx.to_pandas_adjacency(dag, dtype=int))
# nx.draw_networkx(dag)
# plt.show()
"""
