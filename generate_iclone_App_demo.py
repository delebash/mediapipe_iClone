from mediapipe_iclone_converter import *
import os
import json

# main function
with open('./data/python_peace.json') as f:
    json_data = json.load(f)

new_pose = json2iclon(json_data)

# output new pose to txt file
filename = "output.txt"
if os.path.exists(filename):
    os.remove(filename)
else:
    print("The file does not exist")

f = open(filename, 'a')
f.write('frame_data = [ \n')
arr_num = len(new_pose)
for k in range(arr_num):
    pts = new_pose[k]
    for n in range(6):
        strval = str(pts[n]) + "," + '\n'
        f.write(strval)
f.write(']')
f.close()
