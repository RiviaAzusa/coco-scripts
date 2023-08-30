from PIL import Image
import os
import json


def bbox_convert(ori_size, new_size, bbox):
    """
    depend on two size, origin bbox convert to new bbox.
    :param origin_size: (width,height)
    :param new_size: (width,height)
    :param bbox: [x,y,w,h]
    :return: new bbox
    """
    ow, oh = ori_size
    nw, nh = new_size
    x = bbox[0] / ow * nw
    y = bbox[1] / oh * nh
    w = bbox[2] / ow * nw
    h = bbox[3] / oh * nh
    return [x, y, w, h]


def resize_coco_dataset(input_path, output_path, target_height):
    # 创建输出路径
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 复制annotations文件
    annotations_file = os.path.join(input_path, 'annotations.json')
    new_annotations_file = os.path.join(output_path, 'annotations.json')

    # 读取原始annotations数据
    with open(annotations_file, 'r') as f:
        coco_data = json.load(f)

    # 修改annotations中的图片尺寸信息
    images = coco_data['images']
    annotations = coco_data['annotations']
    for image in images:
        img_path = os.path.join(input_path, image['file_name'])
        print(img_path)
        img = Image.open(img_path)
        print(img.size)
        width, height = img.size
        aspect_ratio = float(target_height) / float(height)
        new_width = int(width * aspect_ratio)
        new_height = target_height

        # 将图像resize
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        print(resized_img.size)

        # 保存resize后的图像到输出路径
        new_img_path = os.path.join(output_path, image['file_name'])

        resized_img.save(new_img_path)

        # 更新annotations中的图像尺寸信息
        image['height'] = new_height
        image['width'] = new_width

        for annotation in annotations:
            if annotation['image_id'] == image['id']:
                annotation['bbox'] = bbox_convert(
                    (width, height), (new_width, new_height), annotation['bbox'])
                annotation['area'] = annotation['bbox'][2] * \
                    annotation['bbox'][3]

    # 保存修改后的annotations文件
    with open(new_annotations_file, 'w') as f:
        json.dump(coco_data, f)


# 使用示例
input_path = '/Users/azusa/research/azusa_dataset/figlib_seg/val'
output_path = '/Users/azusa/research/azusa_dataset/figlib_seg/val_1080'
target_height = 1080

resize_coco_dataset(
    input_path=input_path,
    output_path= output_path,
    target_height= target_height
)
