import json
import os

"""
coco_check
input: 
    1.coco annotations json_file
    2.coco images dir
"""


def check(json_file, images_dir):
    with open(json_file, 'r') as f:
        anno_data = json.load(f)
        images = anno_data['images']
        annotations = anno_data['annotations']
        categories = anno_data['categories']
    print('nums of images: {}, nums of annotations: {}'.format(len(images), len(annotations)))
    print('------check the image path------')
    for image in images:
        img_root = os.path.join(images_dir, image['file_name'])
        if not os.path.exists(img_root):
            print('Not existed: ',image["file_name"])
    print('------image path existed------')
    print('------check the annotation------')

    anno_list = []
    img_list = []
    for anno in annotations:
        if anno['id'] in anno_list:
            print('含重复标签: ', anno['id'])
        anno_list.append(anno['id'])

    for img in images:
        if img['id'] in img_list:
            print('含重复图像ID: ', img['id'])
        img_list.append(img['id'])

    for i
    print('Check End')


if __name__ == '__main__':
    # type = 'figlib+nemo'
    json_file='/Users/azusa/research/Azusa_dataset/azusa_dataset/nemo_sc/train.json'
    images_dir = '/Users/azusa/research/Azusa_dataset/azusa_dataset/nemo_sc/train'
    check(json_file, images_dir)
