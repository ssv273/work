import pandas as pd
import numpy as np

df = pd.read_csv('pivot_table.csv')

def pearson(s1, s2):
    s1_correlation = s1-s1.mean()
    s2_correlation = s2-s2.mean()
    return np.sum((s1_correlation*s2_correlation)/np.sqrt(np.sum(s1_correlation**2)*np.sum(s2_correlation**2)))

def get_recs(item_name, df, num):
    scores = []
    for items in df.columns:
        if items == item_name:
            continue
        cor = pearson(df[item_name], df[items])
        if np.isnan(cor):
            continue
        else:
            scores.append((items, cor))

    scores.sort(key=lambda tup: tup[1], reverse=True)
    return scores[:num]



item = input('Введите артикул')

print('С этим товаром чаще всего покупают: ', get_recs(item, df, 5))