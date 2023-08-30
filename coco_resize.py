import cv2 as cv
from tqdm import tqdm
import os
import json
import numpy as np
from pathlib import Path

"""将指定路径的 coco格式数据集 整体resize到指定高度 并复制到一个新路径中, 请注意要同时完成图像的复制和annotations文件的修改"""


def resize_image(image, height_new = 800):
    height, width = image.shape[0], image.shape[1]
    # 设置新的图片分辨率框架
    width_new = int(width / height * height_new)
    # 判断图片的长宽比率
    img_new = cv.resize(image, (width_new, height_new), interpolation=cv.INTER_AREA)
    return img_new

def main(origin_images_path, target_images_path, origin_anno_file, new_height = 800):
    supported_img = ['.jpg']
    origin_images_path = Path(origin_images_path)
    target_images_path = Path(target_images_path)
    target_images_path.mkdir(parents=True, exist_ok = True)

    print('''---- copy resized images to target path ----''')
    for image_file in tqdm(origin_images_path.iterdir()):
        if image_file.suffix not in supported_img:
            continue
        origin_img = cv.imread(str(image_file))
        target_img = resize_image(origin_img)
        cv.imwrite(str(target_images_path/image_file.name), target_img)
    
    print('---- generate new coco-annotations file ----')
    with open(origin_anno_file, 'r') as f:
        total_data = json.load(f)
        total_images = total_data["images"]
        total_categories = total_data["categories"]
        total_annotations = total_data["annotations"]
        image_with_anno = []

        print('依据标签索引图像')
        for idx_anno, anno in tqdm(enumerate(total_data["annotations"])):
            origin_bbox = anno["bbox"]
            image_id = anno["image_id"]
            for idx_img, img in enumerate(total_data["images"]):
                if img['id'] == image_id:
                    image_with_anno.append(img['id'])
                    origin_height = img["height"]
                    origin_width = img["width"]
                    tgt_img_path = os.path.join(target_path, path, img['file_name'])
                    target_h, target_w = cv.imread(tgt_img_path).shape[:2]
                    target_bbox = bbox_convert(origin_size=(origin_width, origin_height),
                                               new_size=(target_w, target_h),
                                               bbox=origin_bbox)
                    area = area_xywh(target_bbox)
                    total_data["annotations"][idx_anno]['area'] = area
                    total_data["annotations"][idx_anno]['bbox'] = target_bbox
                    total_data["images"][idx_img]['height'] = target_h
                    total_data["images"][idx_img]['width'] = target_w
        print('含无标签图像{}个'.format(len(total_data['images']) - len(image_with_anno)))
        print('处理无标签图像')
        for idx_img, img in enumerate(total_data["images"]):
            if img['id'] not in image_with_anno:
                # print('no label：{}'.format(img['file_name']))
                tgt_img_path = os.path.join(target_path, path, img['file_name'])
                target_h, target_w = cv.imread(tgt_img_path).shape[:2]
                total_data["images"][idx_img]['height'] = target_h
                total_data["images"][idx_img]['width'] = target_w

        with open(os.path.join(target_path, path + '.json'), 'w') as f:
            json.dump(total_data, f)         


if __name__ == '__main__':
    origin_images_path = '/Users/azusa/research/azusa_dataset/figlib_seg/val/JPEGImages'
    target_images_path = '/Users/azusa/research/azusa_dataset/figlib_seg/val_resize/JPEGImages'
    origin_anno_file = '/Users/azusa/research/azusa_dataset/figlib_seg/val/annotations.json'
    main(origin_images_path, target_images_path, origin_anno_file)