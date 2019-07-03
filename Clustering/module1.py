import pandas as pd
import numpy as np
import datetime


df = pd.read_csv('sales.csv', sep=';', encoding='PT154', index_col='client_id')
del df['level3']
del df['order_number']

df['item_quantity'] = df['item_quantity'].replace(to_replace=r',', value='.', regex=True).astype('float32')
df['item_sum'] = df['item_sum'].replace(to_replace=r',', value='.', regex=True).astype('float32')

res_df = df.groupby(['client_id', 'level1']).agg({'order_date': 'count', 'item_sum': 'sum'})\
.reset_index()\
.rename(columns={'order_date': 'order_freq', 'level1': 'items_group'})


res_df['items_group_code'] = res_df['items_group'].apply({'одежные ткани': 0,
 'швейная фурнитура': 1,
 'готовые изделия': 2,
 'ткани для дома': 3,
 'технические ткани': 4,
 'выкройки online': 5,
 'мебельные ткани': 6,
 'швейное оборудование': 7}.get)



day = pd.to_datetime(datetime.date.today())

df['days_ago'] = day - pd.to_datetime(df['order_date'])

date_df = df.groupby('client_id').agg('min')

date_df['days_ago'] = (date_df['days_ago'] / np.timedelta64(1, 'D')).astype(int)

del date_df['order_date']
del date_df['item_name']
del date_df['item_quantity']
del date_df['item_sum']
del date_df['level1']

res_df = res_df.merge(date_df, on='client_id')

del res_df['items_group']
res_df.to_csv('res_df.csv')