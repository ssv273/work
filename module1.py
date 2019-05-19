import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import tqdm
import os
from sklearn.model_selection import train_test_split

pallet_eng = {
 'черный': 'black',
 'темный никель': 'dark_nickel',
 'серый': 'gray',
 'серебристый': 'silver',
 'никель': 'nickel',
 'белый': 'white',
 'бежевый': 'beige',
 'медный': 'copper',
 'бронзовый': 'bronze',
 'коричневый': 'brown',
 'терракотовый': 'terracotta',
 'бордовый': 'burgundy',
 'красный': 'red',
 'кислотно-розовый': 'acid_pink',
 'коралловый': 'coral',
 'оранжевый': 'orange',
 'персиковый': 'peach',
 'кремовый': 'cream',
 'молочный': 'lactic',
 'золотистый': 'golden',
 'желтый': 'yellow',
 'кислотный': 'acid',
 'хаки': 'khaki',
 'зеленый': 'green',
 'мятный': 'mint',
 'бирюзовый': 'turquoise',
 'голубой': 'light_blue',
 'синий': 'blue',
 'фиолетовый': 'violet',
 'лиловый': 'lilac',
 'сиреневый': 'purple',
 'фуксия': 'fuchsia',
 'розовый': 'pink'
}

df = pd.read_csv('photo_addr.csv',
                 encoding='PT154', # для windows кодировку поменять на ANSI
                 sep=';')

del df['tone']
df = df.loc[df['color'].isin (pallet_eng.keys()), :]

def df_split(df, color):
    df = df[df['color'] == color].head(150)    #загружаем первые 150 картинок
    df_train, df_val = train_test_split(df, test_size=0.25)   #разбиваем на тест и валид, 0,75/0,25%
    return df_train, df_val

for color in pallet_eng.keys():
    df_train, df_valid = df_split(df, color)
    path_train = r'data/train/' + pallet_eng[color]
    path_val = r'data/val/' + pallet_eng[color]
    if not os.path.exists(path_train):
        os.makedirs(path_train)
    if not os.path.exists(path_val):
        os.makedirs(path_val)
    if df_train.shape[0] != 0:      # оказывается не все цвета из палитры есть
        for i in tqdm.tqdm(range(df_train.shape[0])):
    #         print(color)
            p = requests.get(df_train.iloc[i][2])
            out = open(path_train + '/' + df_train.iloc[i][2].split('/')[-1], "wb")
            out.write(p.content)
            out.close()
    if df_valid.shape[0] != 0:
        for i in tqdm.tqdm(range(df_valid.shape[0])):
            p = requests.get(df_valid.iloc[i][2])
            out = open(path_val + '/' + df_valid.iloc[i][2].split('/')[-1], "wb")
            out.write(p.content)
            out.close()