import json
import os, cv2
from tqdm import tqdm


def generate_bbox(json_path, img_path, path):
    with open(json_path) as annos:
        total_data = json.load(annos)
        images = total_data['images']
        annotations = total_data['annotations']
    print('the annotation_json num_key is:', len(total_data))  # 统计json文件的关键字长度
    print('the annotation_json key is:', total_data.keys())  # 读出json文件的关键字
    print('the annotation_json num_images is:', len(images))  # json文件中包含的图片数量
    print('the annotation_json num_annotations is:', len(annotations))  # json文件中包含的图片数量
    if not os.path.exists(path): os.makedirs(path)
    for anno in tqdm(annotations):
        image_id = anno['image_id']
        bbox_id = anno['id']
        for img in images:
            if img['id'] == image_id:
                image_name = img['file_name']
        image_path = os.path.join(img_path, image_name)  # 拼接图像路径
        image = cv2.imread(image_path, 1)  # 保持原始格式的方式读取图像
        x, y, w, h = anno['bbox']  # 读取边框
        image = cv2.rectangle(image, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 255), 2)
        # image = image[(int(x), int(y)), (int(x + w), int(y + h))]
        subimage = image[int(y):int(y + h), int(x):int(x + w)]
        cv2.imwrite(os.path.join(path, anno['image_id']), subimage)


def visualization_full(json_path, img_path, path):
    with open(json_path) as annos:
        total_data = json.load(annos)
        images = total_data['images']
        annotations = total_data['annotations']
    print('the annotation_json num_key is:', len(total_data))  # 统计json文件的关键字长度
    print('the annotation_json key is:', total_data.keys())  # 读出json文件的关键字
    print('the annotation_json num_images is:', len(images))  # json文件中包含的图片数量
    print('the annotation_json num_annotations is:', len(annotations))  # json文件中包含的图片数量
    if not os.path.exists(path): os.makedirs(path)
    for image in tqdm(images):
        bbox_list = []
        for anno in annotations:
            if anno['image_id'] == image['id']:
                bbox_list.append(anno['bbox'])
        if len(bbox_list) != 0:
            image_path = os.path.join(img_path, image['file_name'])  # 拼接图像路径
            img = cv2.imread(image_path, 1)  # 保持原始格式的方式读取图像
            for bbox in bbox_list:
                x, y, w, h = bbox
                img = cv2.rectangle(img, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 255), 2)

            # cv2.imwrite(os.path.join(path, str(image['file_name'])), img)
            cv2.imwrite(os.path.join(path, image['file_name']), img)
            # cv2.imwrite(os.path.join(path, anno['image_id']), subimage)


if __name__ == "__main__":
    train_path = '/Users/azusa/research/azusa_dataset/figlib_seg/val_800'
    train_json = '/Users/azusa/research/azusa_dataset/figlib_seg/val_800/annotations.json'
    # visualization_full(train_json, train_path, 'figlib_bbox1')
    # generate_bbox(train_json, train_path, 'figlib+nemo')
    visualization_full(train_json, train_path, 'figlib_1080')
    