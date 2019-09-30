from src.main import traverse
import networkx as nx

dag = nx.DiGraph()

dag.add_node("0", label="p1", type="x_node")
dag.add_node("1", label="A", type="leaf")
dag.add_node("2", label="q1", type="x_node")
dag.add_node("3", label="s1", type="y_node")
dag.add_node("4", label="B", type="leaf")
dag.add_node("5", label="p2", type="x_node")
dag.add_node("6", label="C", type="leaf")
dag.add_node("7", label="s2", type="y_node")
dag.add_node("8", label="D", type="leaf")
dag.add_node("9", label="F", type="leaf")
dag.add_node("10", label="q2", type="x_node")
dag.add_node("11", label="s2", type="y_node")
dag.add_node("12", label="E", type="leaf")
dag.add_node("13", label="G", type="leaf")

dag.add_edge("0", "1")
dag.add_edge("0", "2")
dag.add_edge("2", "3")
dag.add_edge("2", "10")
dag.add_edge("3", "4")
dag.add_edge("3", "5")
dag.add_edge("5", "6")
dag.add_edge("5", "7")
dag.add_edge("7", "8")
dag.add_edge("7", "9")
dag.add_edge("10", "11")
dag.add_edge("10", "13")
dag.add_edge("11", "12")
dag.add_edge("11", "9")

traverse()

# nx.draw_networkx(dag)
# plt.show()
