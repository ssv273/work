#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


ratings = pd.read_csv('res.csv', index_col=False)


# In[3]:


ratings = ratings.drop(ratings.columns[0], axis=1)


# In[4]:


ratings.head()


# Генерируем индекс схожести в каждой паре товаров и оставляем только популярные

# In[5]:


userRatings = ratings.pivot_table(index=['client_id'],columns=['item_name'],values='score')


# In[16]:


userRatings.to_csv('userRatings.csv')


# In[6]:


# обратить внимание на min_periods - это минимальное количество оценок для товара 
# для включения его в матрицу корреляций!!!!
corrMatrix = userRatings.corr(method='pearson', min_periods=5)


# In[14]:


corrMatrix.to_csv('corrMatrix.csv')

