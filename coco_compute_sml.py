import json
"""
统计COCO格式数据集中的大中小个数
coco:
    s: [0,32*32]
    m: [32*32,96*96]
    l: [96*96:]
ratio:
    s: r < 0.005
    m: 0.005 < r < 0.01
    l: r > 0.01
"""

if __name__=='__main__':
    # anno_file='/Users/azusa/research/azusa_dataset/figlib_useless/figlib/val.json'
    anno_file = '/Users/azusa/research/azusa_dataset/figlib_seg/val/annotations.json'
    coco_dic={'s':0,'m':0,'l':0}
    ratio_dic={'s':0,'m':0,'l':0}
    coco_resize={'s':0,'m':0,'l':0}

    with open(anno_file, 'r') as f:
        anno_data = json.load(f)
        images = anno_data['images']
        annotations = anno_data['annotations']
        print(len(images),len(annotations))
    for anno in annotations:
        w,h=anno['bbox'][2:]
        for image in images:
            if image['id']==anno['image_id']:
                area=image['height']*image['width']
                w1=1080/image['width']*w
                h1=1920/image['height']*h
        if w*h>96**2:
            coco_dic['l']+=1
        elif w*h>32**2:
            coco_dic['m']+=1
        else:
            coco_dic['s']+=1

        if w1*h1>96**2:
            coco_resize['l']+=1
        elif w1*h1>32**2:
            coco_resize['m']+=1
        else:
            coco_resize['s']+=1
        r=w*h/area
        if r>0.01:
            ratio_dic['l']+=1
        elif r>0.005:
            ratio_dic['m']+=1
        else:
            ratio_dic['s']+=1
    print('coco: ',coco_dic)
    print('coco_resize: ',coco_resize)
    print('ratio: ',ratio_dic)
