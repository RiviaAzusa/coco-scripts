import json
from re import sub


val_fires='/Users/azusa/research/azusa_dataset/figlib_useless/FIgLib_split_file_2/train_fires.txt'
json_file='/Users/azusa/research/azusa_tools/analyse/figlib_new/annotations.json'

with open(json_file,'r') as f:
    data=json.load(f)
    images=data['images']
for image in images:
    image['file_name']=sub(r'JPEGImages/','',image['file_name'])
    print(image)
with open('val.json','w') as f:
    json.dump(data,f)

