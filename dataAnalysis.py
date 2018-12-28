import pandas as pd
import numpy as np
import networkx as nx
import matplotlib as plt

gg_data = pd.read_csv('C:/Users/prate/Desktop/ML Projects/GroupGiri/data.csv')
#gg_data.head()
#gg_data.nunique()
gg_data = gg_data.drop([u'name'],axis=1)
gg_data_no_duplicates = gg_data.T.drop_duplicates().T
quit()
#gg_data_no_duplicates.columns
#gg_data_no_duplicates.nunique()
#gg_data_no_duplicates.shape
#gg_data_no_duplicates.account_status.value_counts()
#gg_data_no_duplicates.loc[gg_data_no_duplicates['account_status'] == 'active']
subset = gg_data[['user_id', 'friend_id']]
node_pairs = [tuple(x) for x in subset.values]
node_array = gg_data.as_matrix(columns=['user_id']).T[0]
Graph = nx.Graph()
Graph.add_nodes_from(node_array)
Graph.add_edges_from(node_pairs)