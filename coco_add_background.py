'''
from val_fires.txt to add background img to coco json
'''
import json
from pathlib import Path
import cv2 as cv

json_file='figlib_new/val.json'
images_path='/Users/azusa/research/azusa_dataset/figlib_useless/figlib/val'
images_path=Path(images_path)
image_files=[i for i in images_path.iterdir() if i.suffix=='.jpg' and '+' not in str(i)]
print(len(image_files))
with open(json_file,'r') as f:
    data=json.load(f)
    images=data['images']
id=240
for image in image_files:
    
    cv_img=cv.imread(str(image))
    height,width=cv_img.shape[0],cv_img.shape[1]
    i= {       
            "license": 0,
            "url": None,
            "file_name": str(image).split('/')[-1],
            "height": height,
            "width": width,
            "date_captured": None,
            "id": id
        }
    images.append(i)
    id+=1

with open('val1.json','w') as f:
    json.dump(data,f)



