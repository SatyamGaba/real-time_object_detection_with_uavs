#
# ---------------------------------------------------------------------------------
# Filename:        testing_annotations.py
# Project name:    Real-time applications of Computer Vision on UAVs
# Author:          Satyam Gaba (satyamgb321@gmail.com)
# Supervisor:      Pratik Narang
# Last modified:   25 May 2019
# Comments:        This file contains the python script that can be used to verify
#                  the modified datset. It will plot bounding boxes on an image
#                  which can be verified manually.
# ---------------------------------------------------------------------------------

import csv
import os
import cv2
from os import walk


pred_annot_dir = r'E:\Large Data\real_time_object\#Dataset\VisDrone\predictions'
img_dir = r'E:\Large Data\real_time_object\#Dataset\VisDrone\train_final'





_,_,image_ids = next(walk(img_dir))
image_ids = [i[:-4] for i in image_ids]
image_ids = sorted(image_ids)

#print(image_ids)

image_id = 0
threshold = 0.3
boxs = []
with open(os.path.join(pred_annot_dir,image_ids[image_id])+".txt", 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter = ' ', lineterminator = '\n') 
    for row in csvreader:
        if float(row[1]) >= threshold:
            boxs.append([int(row[0]),int(row[2]),int(row[3]),int(row[4]),int(row[5])])


cv2.rectangle(os.path.join(img_dir,image_ids[image_id])+".jpg",(384,0),(510,128),(0,255,0),3)