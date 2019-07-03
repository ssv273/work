
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

df = pd.read_csv('res_df.csv', index_col='client_id')
df = df.drop(df.columns[0], axis=1)

scaler = StandardScaler()

df_scaled = scaler.fit_transform(df)



tsne = TSNE(n_components=2, learning_rate=250, random_state=42)

df_scaled_tsne = tsne.fit_transform(df_scaled)

num_clasters = 5


kmeans = KMeans(n_clusters=num_clasters, max_iter=100, random_state=42).fit(df_scaled_tsne)

labels = kmeans.fit_predict(df_scaled_tsne)

df['class'] = 0
for a in range(num_clasters):
    df['class'][labels == a] = a

print(df.groupby('class').agg({'order_freq':['min', 'max', 'mean'],
                        'item_sum':['min', 'max', 'mean'],
                        'items_group_code':'unique',
                        'days_ago':['min', 'max', 'mean']
                        }))