from __future__ import print_function, division

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy
from PIL import Image
from io import BytesIO


the_model = torch.load('model.mod')

image = input('Вставьте путь до рисунка на диске')   # тупо вставить полный путь до рисунка на диске

img = Image.open(image)

transforms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

img_tr = transforms(img)
img_tr = torch.unsqueeze(img_tr,0)
pred = the_model(img_tr)
res = ['acid',
 'acid_pink',
 'beige',
 'black',
 'blue',
 'bronze',
 'brown',
 'burgundy',
 'copper',
 'coral',
 'cream',
 'dark_nickel',
 'fuchsia',
 'golden',
 'gray',
 'green',
 'khaki',
 'lactic',
 'light_blue',
 'lilac',
 'mint',
 'nickel',
 'orange',
 'peach',
 'pink',
 'purple',
 'red',
 'silver',
 'terracotta',
 'turquoise',
 'violet',
 'white',
 'yellow']

res[int(pred.max(1)[1])]