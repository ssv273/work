import requests
from PIL import Image
from io import BytesIO
import numpy as np
import pandas as pd
import tqdm

def prepare_image(url,size=(100,100)):
    p = requests.get(url)
    i = Image.open(BytesIO(p.content))
    i = i.resize(size)
    arr = np.asarray(i, dtype='uint8')
    return arr

def compute_distance(arr, pallet):
    distance_L1 = dict.fromkeys(pallet.keys())
    distance_L2 = dict.fromkeys(pallet.keys())
    df_L1 = pd.DataFrame(columns=pallet.keys())
    df_L2 = pd.DataFrame(columns=pallet.keys())
    count = 0
    for n in tqdm.tqdm(range(arr.shape[0])):
        for m in range(arr.shape[1]):
            for i in pallet:
                distance_L1[i] = np.abs(arr[n, m, 0]-pallet[i][0])+np.abs(
                    arr[n, m, 1]-pallet[i][1])+np.abs(arr[n, m, 2]-pallet[i][2])
                distance_L2[i] = np.sqrt((arr[n, m, 0]-pallet[i][0])**2+(
                    arr[n, m, 1]-pallet[i][1])**2 + (arr[n, m, 2]-pallet[i][2])**2)
            df_L1.loc[count] = distance_L1
            df_L2.loc[count] = distance_L2
            count = count + 1
    df_L1_summ = pd.DataFrame(df_L1.sum()).reset_index().rename(columns={0:'summ', 'index':'colour'})
    summ_df_L1_summ = df_L1_summ['summ'].sum()
    df_L1_summ['percent'] = df_L1_summ['summ']/float(summ_df_L1_summ)/100
    df_L2_summ = pd.DataFrame(df_L2.sum()).reset_index().rename(columns={0:'summ', 'index':'colour'})
    summ_df_L2_summ = df_L2_summ['summ'].sum()
    df_L2_summ['percent'] = df_L2_summ['summ']/float(summ_df_L2_summ)/100
    res_L1 = df_L1_summ.loc[df_L1_summ['summ'] == df_L1_summ['summ'].min()]
    res_L2 = df_L2_summ.loc[df_L2_summ['summ'] == df_L2_summ['summ'].min()]
    print('Наболее вероятный цвет {}, по метрике L1'.format(res_L1.colour.values[0]))
    print('Наболее вероятный цвет {}, по метрике L2'.format(res_L2.colour.values[0]))


pallet = {'red': [255, 0, 0], 'orange': [255, 165, 0], 'yellow': [255, 255, 0], 'green': [0, 255, 0],
          'blue': [0, 0, 255], 'dark blue': [0, 0, 139], 'purple': [160, 32, 240],
          'black': [0, 0, 0], 'white': [255, 255, 255], 'SkyBlue':[135,206,235], 'PeachPuff':[255,218,185]}

url = input('Введите URL картинки  ')

arr = prepare_image(url)
compute_distance(arr, pallet)