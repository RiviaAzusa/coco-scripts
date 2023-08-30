"""
将 coco 数据集中的图像复制到某个文件夹
适合从一大堆图像文件中筛选某些图的操作：）
"""
import json
import os
from tqdm import tqdm

if __name__ == '__main__':
    coco_json = 'cocolabel2/train.json'
    origin_path = '/Users/azusa/research/Azusa_dataset/figlib'
    target_path = '/Users/azusa/research/MySmokeDetectModel/data_analyse/dataset/temp'
    if not os.path.exists(target_path):os.makedirs(target_path)
    with open(coco_json, 'r') as f:
        total_data = json.load(f)
    for img in tqdm(total_data['images']):
        fn = img['file_name'].replace('../', '')
        origin_file = os.path.join(origin_path, fn)
        file_name = img['file_name'].split('/')[-2] + '--' + img['file_name'].split('/')[-1]
        print(file_name)
        target_file = os.path.join(target_path, file_name)
        if not os.path.exists(origin_file): print('No this file :{}\n'.format(origin_file))
        os.system('cp ' + origin_file + ' ' + target_file)
