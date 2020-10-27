# !pip
# install
# paddlex - i
# https: // mirror.baidu.com / pypi / simple
# !pip
# install
# imgaug - i
# https: // mirror.baidu.com / pypi / simple

import functools
import os
import shutil
import sys
import tarfile
import time
import zipfile

import requests

lasttime = time.time()
FLUSH_INTERVAL = 0.1

# download_file_and_uncompress("https://paddleseg.bj.bcebos.com/models/xception65_coco.tgz", './pretrained_model/xception65_coco.tgz', "./pretrained_model/", extraname="xception")

# 设置使用0号GPU卡（如无GPU，执行此代码后仍然会使用CPU训练模型）
import matplotlib
import os
import paddlex as pdx

os.environ['CUDA_VISIBLE_DEVICES'] = '0'

from paddlex.seg import transforms
import imgaug.augmenters as iaa

train_transforms = transforms.Compose([
    transforms.Resize(target_size=300),
    transforms.RandomPaddingCrop(crop_size=256),
    transforms.RandomBlur(prob=0.1),
    transforms.RandomRotate(rotate_range=15),
    # transforms.RandomDistort(brightness_range=0.5),
    transforms.RandomHorizontalFlip(),
    transforms.Normalize()
])
eval_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.Normalize()
])

# !unzip data/data55723/img_testA.zip
# !unzip data/data55723/train_data.zip

# !unzip train_data/lab_train.zip
# !unzip train_data/img_train.zip

import numpy as np

datas = []
image_base = 'img_train'
annos_base = 'lab_train'

ids_ = [v.split('.')[0] for v in os.listdir(image_base)]

for id_ in ids_:
    img_pt0 = os.path.join(image_base, '{}.jpg'.format(id_))
    img_pt1 = os.path.join(annos_base, '{}.png'.format(id_))
    datas.append((img_pt0.replace('/home/aistudio/work/', ''), img_pt1.replace('/home/aistudio/work/', '')))
    if os.path.exists(img_pt0) and os.path.exists(img_pt1):
        pass
    else:
        raise "path invalid!"

print('total:', len(datas))
print(datas[0][0])
print(datas[0][1])

data_dir = '/home/aistudio/work/'

import numpy as np

labels = [
    '建筑', '耕地', '林地',
    '水体', '道路', '草地',
    '其他'
]

with open('labels.txt', 'w') as f:
    for v in labels:
        f.write(v + '\n')

np.random.seed(5)
np.random.shuffle(datas)

split_num = int(0.02 * len(datas))

train_data = datas[:-split_num]
valid_data = datas[-split_num:]

with open('train_list.txt', 'w') as f:
    for img, lbl in train_data:
        f.write(img + ' ' + lbl + '\n')

with open('valid_list.txt', 'w') as f:
    for img, lbl in valid_data:
        f.write(img + ' ' + lbl + '\n')

print('train:', len(train_data))
print('valid:', len(valid_data))

data_dir = './'

train_dataset = pdx.datasets.SegDataset(
    data_dir=data_dir,
    file_list='train_list.txt',
    label_list='labels.txt',
    transforms=train_transforms,
    shuffle=True)

eval_dataset = pdx.datasets.SegDataset(
    data_dir=data_dir,
    file_list='valid_list.txt',
    label_list='labels.txt',
    transforms=eval_transforms)

num_classes = len(train_dataset.labels)
model = pdx.seg.DeepLabv3p(
    num_classes=num_classes, backbone='Xception65', use_bce_loss=False
)
model.train(
    num_epochs=100,
    train_dataset=train_dataset,
    train_batch_size=4,
    eval_dataset=eval_dataset,
    learning_rate=0.0002,
    save_interval_epochs=1,
    save_dir='output/deeplab',
    log_interval_steps=200,
    pretrain_weights='pretrained_model/xception')

model.evaluate(eval_dataset, batch_size=1, epoch_id=None, return_details=False)

# model = pdx.load_model('./output/deeplab/best_model')

from tqdm import tqdm
import cv2

test_base = 'img_testA/'
out_base = 'ccf_baidu_remote_sense/results/'

if not os.path.exists(out_base):
    os.makedirs(out_base)

for im in tqdm(os.listdir(test_base)):
    if not im.endswith('.jpg'):
        continue
    pt = test_base + im
    result = model.predict(pt)
    cv2.imwrite(out_base + im.replace('jpg', 'png'), result['label_map'])
