import pandas as pd
import numpy as np
import pyfpgrowth
import sys
import json


sys.setrecursionlimit(10000000)

df = pd.read_csv('sales.csv', sep = ';', encoding='PT154')

df_1 = df.loc[df['level1'] == 'ткани для дома']

product_ids = df_1['item_name'].unique()

def scale_item_id(product_id):
    scaled = np.where(product_ids == product_id)[0][0] + 1
    return scaled

df_1['item_name'] = df_1['item_name'].apply(scale_item_id)

res_df = df_1.groupby('order_number'). agg({'item_name':'unique'})

patterns = pyfpgrowth.find_frequent_patterns(res_df['item_name'],3)

a = pyfpgrowth.generate_association_rules(patterns, 0.7)

np.save('patterns.npy', a)

# read_dictionary = np.load('patterns.npy').item()



#a[(2013,)]


# In[16]:


# read_dictionary[(2013,)]

