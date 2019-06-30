#!/usr/bin/env python
# coding: utf-8

# In[55]:


import pandas as pd
import numpy as np


# In[56]:


ratings = pd.read_csv('res.csv', index_col=False)


# In[57]:


ratings = ratings.drop(ratings.columns[0], axis=1)


# In[58]:


ratings.head()


# In[5]:


product_Ratings = ratings.pivot_table(index=['client_id'],columns=['item_name'],values='score')


# In[6]:


product_Ratings.describe()


# #### генерируем индекс схожести (корреляции) между выбранным товаром и всеми остальными 

# In[7]:


product_code = 'АКС-1-27'


# In[8]:


item_Rating = product_Ratings[product_code]


# In[9]:


product_Ratings.head()


# In[10]:


similar_Products = product_Ratings.corrwith(item_Rating)


# In[11]:


similar_Products = similar_Products.dropna()


# In[12]:


df = pd.DataFrame(similar_Products)


# In[13]:


df.head()


# #### группируем по количеству оценок и выводим среднюю оценку

# In[38]:


product_Stats = ratings.groupby('item_name').agg({'score': [np.size, np.mean]}) 


# In[39]:


product_Stats.head()


# #### Удаляем непопулярные товары, чтобы система не подкидывала нам неподходящих рекомендаций
# 

# In[50]:


ratingsCount = product_Stats['score']['size'].max()/5*3


# #### получаем только те товары, количество оценок которых более ratingsCount
# 

# In[51]:


popular_Products = product_Stats['score']['size'] >= ratingsCount


# In[52]:


popular_Products.head()


# #### получаем первые 15 товаров оцененных более ratingsCount раз и отсортированных по убыванию оценки

# In[53]:


product_Stats[popular_Products].sort_values([('score', 'mean')], ascending=False)[:15]


# In[ ]:




