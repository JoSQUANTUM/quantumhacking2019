import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from(["USD", "EURO", "CAD"])

G.add_edges_from([("USD", "EURO"), ("USD", "CAD"), ("EURO", "CAD")])
#                  ("GBP", "USD"), ("GBP", "EURO"), ("GBP", "CAD")])

pos = nx.spring_layout(G)
nx.draw_networkx(G, pos, True)
nx.draw_networkx_edge_labels(G, pos, edge_labels={("USD", "EURO"): '0.91 / 1.10',
("CAD", "EURO"): '1,46 / 0.68', ("USD", "CAD"): '1.33 / 0.75'}, font_color='red')
plt.axis('off')
plt.show()