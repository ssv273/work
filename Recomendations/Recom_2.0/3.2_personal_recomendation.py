#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# # Предлагаем пользователю рекомендации в зависимости от проставленных им оценок

# грузим данные

# In[2]:


userRatings = pd.read_csv('userRatings.csv', index_col='client_id')


# In[3]:


corrMatrix = pd.read_csv('corrMatrix.csv', index_col = 'item_name')


# Генерируем рекомендации для каждого товара, просмотренного и оцененного нашим пользователем (здесь – данные для пользователя 14795) 

# In[4]:


user_ID = 14795
myRatings = userRatings.loc[user_ID].dropna()


# In[5]:


simCandidates = pd.Series()
for i in range(0, len(myRatings.index)):
	    # Извлекаем товары, похожие на оцененные этим пользователем
    sims = corrMatrix[myRatings.index[i]].dropna()
	    # Далее оцениваем их сходство в зависимости от того, как он оценил тот или иной товар
    sims = sims.map(lambda x: x * myRatings[i])
	    # Добавляем индекс в список сравниваемых кандидатов
    simCandidates = simCandidates.append(sims)


# In[6]:


simCandidates.sort_values(inplace = True, ascending = False)


# Суммируем показатели идентичных товаров

# In[7]:


simCandidates = simCandidates.groupby(simCandidates.index).sum()
simCandidates.sort_values(inplace = True, ascending = False)


# Оставляем лишь те товары, которые пользователь еще не покупал

# In[8]:


filteredSims = simCandidates.drop(myRatings.index, errors='ignore')


# In[9]:


print(filteredSims)

