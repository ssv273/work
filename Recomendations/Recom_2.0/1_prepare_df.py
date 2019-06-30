import pandas as pd
import numpy as np
from tqdm import tqdm


# In[2]:


df = pd.read_csv('recom.csv', sep=';', encoding='PT154')


# In[3]:


df['item_quantity'] = df['item_quantity'].replace(
    to_replace=r',', value='.', regex=True).astype('float32')


# In[4]:


del df['order_number']
del df['order_date']
del df['level3']


# In[5]:


c = df.groupby(['level1', 'client_id', 'item_name'], as_index=False).agg('sum')


# In[6]:


fabric = c.loc[(c.level1 == 'ткани для дома') | (c.level1 == 'одежные ткани') | (
    c.level1 == 'технические ткани') | (c.level1 == 'мебельные ткани'), ['client_id', 'item_name', 'item_quantity']]


# In[7]:


def scores(df, id_client):
    b = df.loc[df.client_id == id_client]
    b['score'] = np.ceil(b['item_quantity'] / b['item_quantity'].max() * 10)
    return b


# In[8]:


res = pd.DataFrame(columns=('client_id', 'item_name', 'item_quantity', 'score'))


# In[9]:


clients_list = fabric.client_id.unique()


# In[10]:


for i in tqdm(clients_list):
    res = res.append(scores(fabric, i), ignore_index=True)


# In[11]:


res.shape, fabric.shape


# In[12]:


del res['item_quantity']




# In[14]:


res.to_csv('res.csv')

