import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import community

gg_data = pd.read_csv('adata_1jan.csv')
gg_data.head()
result = gg_data.sort_values(by=['friend_id'])

node_list = set(gg_data['user_id'].values.tolist())

edge_array = gg_data[['user_id','friend_id']].values
edge_tuple = tuple(map(tuple, edge_array))

Graph = nx.Graph()
Graph.add_edges_from(edge_tuple)

node_attr = {}
for index, row in gg_data.iterrows():
    node_attr[row['user_id']] = {'status': row['active']}
    node_attr[row['friend_id']] = {'status': row['account_status']}

print nx.info(Graph)

remove = [node for node,degree in Graph.degree() if degree < 2]
Graph.remove_nodes_from(remove)
remove_0 = [node for node,degree in Graph.degree() if degree < 1]
Graph.remove_nodes_from(remove_0)
print nx.info(Graph)

nodes_to_keep = []
for node in Graph.nodes():
    if Graph.degree(node) > 600:
        nodes_to_keep.append(node)

edge_list = list(Graph.edges())
for index, val in enumerate(edge_list):
    if val[0] in nodes_to_keep:
        pass 
    else:
        del edge_list[index]

newGraph = nx.Graph()

newGraph.add_edges_from(edge_list)
print nx.info(newGraph)

nx.set_node_attributes(newGraph, node_attr)
active_nodes = [n for (n,s) in nx.get_node_attributes(newGraph,'status').iteritems() if s == 'active']
ghost_nodes = [n for (n,s) in  nx.get_node_attributes(newGraph,'status').iteritems() if s == 'ghost']

#Create network layout for visualizations
spring_pos = nx.spring_layout(newGraph)

plt.axis("off")
d=dict(nx.degree(newGraph))
nx.draw_networkx(newGraph, pos = spring_, nodelist=d.keys(),\
node_color = ['blue' if n==12 else 'green' if newGraph.node[n]['status'] == 'ghost' else 'red' for n in d.keys()],\
with_labels = False, node_size=[v for v in d.values()], width = 0.1)
plt.show()

nx.write_gexf(newGraph, "GG_visualize.gexf")

parts = community.best_partition(newGraph)
values = [parts.get(node) for node in newGraph.nodes()]

plt.axis("off")
nx.draw_networkx(newGraph, pos = spring_pos, cmap = plt.get_cmap("jet"), \
node_color = values, node_size = 35, with_labels = False)
plt.show()
