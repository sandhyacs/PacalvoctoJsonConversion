import pandas as pd
import os,json
import glob

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

with open('keypoints.json', 'w') as outfile:
	json.dump(keypoints_json, outfile)
