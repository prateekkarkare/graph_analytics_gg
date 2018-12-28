import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import community
import operator

gg_data = pd.read_csv('adata_24dec.csv')

#result = gg_data.sort_values(by=['friend_id'])
#node_list = set(gg_data['user_id'].values.tolist())
edge_array = gg_data[['user_id','friend_id']].values
edge_tuple = tuple(map(tuple, edge_array))

Graph = nx.Graph()

Graph.add_edges_from(edge_tuple)

node_attr = {}
for index, row in gg_data.iterrows():
    node_attr[row['user_id']] = {'status': row['account_status']}
    node_attr[row['friend_id']] = {'status': row['account_status.1']}

nx.set_node_attributes(Graph, node_attr)
print nx.info(Graph)
remove = [node for node,degree in Graph.degree() if degree < 2]
Graph.remove_nodes_from(remove)
remove_0 = [node for node,degree in Graph.degree() if degree < 1]
Graph.remove_nodes_from(remove_0)
print nx.info(Graph)

active_nodes = [n for (n,s) in nx.get_node_attributes(Graph,'status').iteritems() if s == 'active']
ghost_nodes = [n for (n,s) in  nx.get_node_attributes(Graph,'status').iteritems() if s == 'ghost']

#Create network layout for visualizations
spring_pos = nx.spring_layout(Graph)

plt.axis("off")
d=dict(nx.degree(Graph))
nx.draw_networkx(Graph, pos = spring_pos, nodelist=d.keys(), \
node_color = ['green' if Graph.node[n]['status'] == 'ghost' else 'red' for n in d.keys()], \
with_labels = False, node_size=[v for v in d.values()])
plt.show()

parts = community.best_partition(Graph)
values = [parts.get(node) for node in Graph.nodes()]
plt.axis("off")
nx.draw_networkx(Graph, pos = spring_pos, cmap = plt.get_cmap("jet"), node_color = values, node_size = 35, with_labels = False)
plt.show()

adj_matrix = nx.adjacency_matrix(Graph)
plt.imshow(adj_matrix.todense())
plt.show()

nx.write_gexf(Graph, "gg_social.gexf")

bc_value = nx.betweenness_centrality(Graph, endpoints=True)

sorted_bc_val = sorted(bc_value.items(), key=operator.itemgetter(1), reverse=True)
sorted_bc_val = [list(l) for l in sorted_bc_val]
for l in sorted_bc_val:
    l.append(node_attr[l[0]]['status'])
