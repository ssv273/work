import pandas as pd
import numpy as np

df = pd.read_csv('recom.csv', sep=';', encoding='PT154')

df['item_quantity'] = df['item_quantity'].replace(
    to_replace=r',', value='.', regex=True).astype('float32')

del df['order_number']
del df['order_date']
del df['level3']

c = df.groupby(['level1', 'client_id', 'item_name'], as_index=False).agg('sum')
fabric = c.loc[(c.level1 == 'ткани для дома') | (c.level1 == 'одежные ткани') | (
    c.level1 == 'технические ткани') | (c.level1 == 'мебельные ткани'), ['client_id', 'item_name', 'item_quantity']]

def scores(df, id_client):
    b = df.loc[df.client_id == id_client]
    b['score'] = round(b['item_quantity'] / b['item_quantity'].max() * 5)
    return b

res = pd.DataFrame(columns=('client_id', 'item_name', 'item_quantity', 'score'))
clients_list = fabric.client_id.unique()

for i in clients_list:
    res = res.append(scores(fabric, i), ignore_index=True)

del res['item_quantity']

df_table = res.pivot_table(index='client_id', columns='item_name', values='score', aggfunc='sum')

df_table.to_csv('pivot_table.csv')