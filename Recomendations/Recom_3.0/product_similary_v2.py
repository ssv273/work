#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import numpy as np
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')



ratings = pd.read_csv('res.csv')


# Этап 1: Находим похожие товары


productRatings = ratings.pivot_table(index=['client_id'],columns=['item_name'],values='score')



def similar_products_func(product, num_similar_products=15):
    fabric_Ratings = productRatings[product]
    similar_Products = productRatings.corrwith(fabric_Ratings)
    similar_Products = similar_Products.dropna()
    df = pd.DataFrame(similar_Products)
    # Удаляем непопулярные товары, чтобы система не подкидывала нам неподходящих рекомендаций
    ratingsCount = 4
    # группируем по количеству оценок и выводим среднюю оценку
    fabric_Stats = ratings.groupby('item_name').agg({'score': [np.size, np.mean]}) 
    # получаем только те товары, количество оценок которых более ratingsCount
    popular_products = fabric_Stats['score']['size'] >= ratingsCount 
    # получаем первые 15 товаров с оцененных более ratingsCount раз и отсортированных по убыванию оценки
    fabric_Stats[popular_products].sort_values([('score', 'mean')], ascending=False)[:15]
    # Извлекаем популярные товары, похожие на целевой
    df = fabric_Stats[popular_products].join(pd.DataFrame(similar_Products, columns=['similarity'])).reset_index()
    return df


def get_tables_similar_products(item_name, num_similar_products=15):
    df = similar_products_func(item_name)
    df = df.rename(columns={('score', 'mean'):'mean', ('score', 'size'):'count'})
    df = df.sort_values(['similarity'], ascending=False)[:num_similar_products]
    df = df[df['similarity']>0.7] # отбираем только те товары похожесть которых более 0,7
    df = df.sort_values(['mean', 'similarity'], ascending=False)
    del df['count']
    del df['mean']
    del df['similarity']
    return df


# # Этап 2: определяем наиболее популярные товары

rate = ratings.groupby('item_name').agg({'score': ['count', 'mean','min', 'max']})
rate = rate.sort_values([('score','count'),('score', 'mean')], ascending=False).head(15)
rate = rate.sort_values([('score', 'mean')], ascending=False)
rate = rate.droplevel(level=0, axis=1)
del rate['count']
del rate['mean']
del rate['min']
del rate['max']


# # Создаём общую табличку по всем товарам

name_columns_list = []
for i in range(1, 16):
    name = 'product_' + str(i)
    name_columns_list.append(name)

res_df = pd.DataFrame(columns=name_columns_list)
items_list = ratings.item_name.unique()

for items in tqdm(items_list):
    res = get_tables_similar_products(items)
    res_full = res.append(rate.reset_index()[:(15-res.shape[0])]).reset_index()
    dict_list = []
    for i in range(15):
        dict_list.append(res_full.iloc[i][1])
    res_df.loc[items] = dict_list

res_df.to_csv('res_table.csv')

