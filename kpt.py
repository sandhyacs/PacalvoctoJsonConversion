import pandas as pd
import os,json
import glob
from collections import Counter

json_list = os.listdir("./annotations/__annotations_merged/")
points_x = []
points_y = []
file_name = []
keypoints = []
keypoints_json = []
for idx, file in enumerate(json_list):
	imgname = file.rsplit(".",1)[0]
	print(imgname)
	df = pd.read_json("./annotations/__annotations_merged/{}".format(file))

	# print(df['left_wrist_center']['coordinates'])
	file_name.append(imgname)
	points_x.append(df['left_wrist_center']['coordinates']['x'])
	points_y.append(df['left_wrist_center']['coordinates']['y'])


for i in range(1, len(points_x)):
	keypoints.append([points_x[i], points_y[i], 2])

for i in range(1, len(keypoints)):
	kpt = {
		"file_name" : file_name[i],
		"keypoints" : keypoints[i]
	}
	keypoints_json.append(kpt)

print(keypoints_json)

# with open('keypoints.json', 'w') as outfile:
# 	json.dump(keypoints_json, outfile)



box_json= open("./instances_train.json")
data_box = json.loads(box_json.read())
kpt_json = open("./keypoints.json")
data_kpt = json.loads(kpt_json.read())


print(data_box.keys())
print(data_box["images"][0])
print(data_box["annotations"][0])
print(len(data_box["images"]), len(data_box["annotations"]))
print(len(data_kpt))
print(data_kpt[0])
imagenames_data_kpt = [x['file_name'] for x in data_kpt]
print(len(imagenames_data_kpt), imagenames_data_kpt[:2])

#'images', 'type', 'annotations', 'categories']
images_data_box = [x for x in data_box['images'] if x['file_name'] in imagenames_data_kpt]
#{'file_name': 'rashmi000106_handData.png', 'height': 780, 'width': 1040, 'id': 298}
# print(len(images_data_box), images_data_box[:2])
image_id = [x['id'] for x in images_data_box]
print(len(image_id))
annotations_data_box = [x for x in data_box['annotations'] if x['image_id'] in image_id]
# print(len(annotations_data_box), annotations_data_box[:2])
# annotations_data_box_id = [x['image_id'] for x in annotations_data_box]
# print(len(annotations_data_box_id), len(set(annotations_data_box_id)))
# print(dict(Counter(annotations_data_box_id)))
# for x in [x for x in data_box['annotations'] if x['image_id'] in [556,557]]:
# 	print(x)
data_kpt_iddict=dict()

for imgid in image_id:
	imgfilename = [x['file_name'] for x in images_data_box if x['id'] == imgid][0]
	kpt_val = [x for x in data_kpt if x['file_name']==imgfilename]
	#print("Data == ", imgid, imgfilename, kpt_val)
	data_kpt_iddict[imgid] = kpt_val
# print(data_kpt_iddict[557])
#annotations_data_box_mod = [x['keypoints']=data_kpt_iddict[x['image_id']][0]['keypoints'] for x in annotations_data_box]
annotations_data_box_mod = []
for x in annotations_data_box:
	x['keypoints'] = data_kpt_iddict[x['image_id']][0]['keypoints']
	x['num_keypoints'] = 1
	annotations_data_box_mod.append(x)
	#print(x.keys())
    
# print(annotations_data_box_mod[:2])
# print(images_data_box[:2])
data_box['images'] = images_data_box
data_box['annotations'] = annotations_data_box_mod
print(type(data_box))
with open('handkpt117.json', 'w') as f:
	f.write(json.dumps(data_box))
'''
imgname = []
img_id = []
for i in data_box["images"]:
	imgname.append(i["file_name"])
	img_id.append(i["id"])
kpt_imgname = []
kpt_pt = []
annot_id =[]
for ann in data_box["annotations"]:
	annot_id.append(ann["image_id"])


for j in data_kpt:
	kpt_imgname.append(j["image_name"])
	kpt_pt.append(j["keypoints"])

for d in data_box["images"]:
	for a,b in zip(kpt_imgname, kpt_pt):
		if d["file_name"]==a:
			print("matched")
			for i in annot_id:
				if d["id"]==i:
					print("id matched")
					print(i, a,b)
'''
