import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

gg_data = pd.read_csv('adata_24dec.csv')

gg_data.head()

gg_data.nunique()

gg_data.account_status.value_counts()

gg_data.loc[gg_data['account_status'] == 'active'];

mydict = {}
for index, row in gg_data.iterrows():
    try:
        val = mydict[row['friend_id']]
        val.append(row['user_id'])
        mydict.update({row['friend_id']:val})
    except KeyError:
        val = [row['user_id']]
        mydict.update({row['friend_id']:val})

hist_dict = {}
for key, value in mydict.iteritems():
    try:
        new_key = len(mydict[key])
        count   = hist_dict[new_key]
        count+=1
        hist_dict.update({new_key:count})
    except KeyError:
        new_key = len(mydict[key])
        hist_dict.update({new_key:1})

len(hist_dict)

hist_dict
del hist_dict[1]
del hist_dict[2]

plt.bar(hist_dict.keys(), hist_dict.values(), 0.5, color='g', align='center')
plt.ylabel('Number of users')
plt.xlabel('Number of Active Contacts')
plt.show()


