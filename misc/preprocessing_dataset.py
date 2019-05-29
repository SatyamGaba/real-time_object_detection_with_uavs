#
# ---------------------------------------------------------------------------------
# Filename:        preprocessing_dataset.py
# Project name:    Real-time applications of Computer Vision on UAVs
# Author:          Satyam Gaba
# Supervisor:      Pratik Narang
# Last modified:   25 May 2019
# Comments:        This file contains the python script that modifies the dataset of
#                  aiskeye in the appropriate format for the object detection script
#                  The script will need to run once initially.
# ---------------------------------------------------------------------------------

import os
import csv
import random
from shutil import copyfile
from os import listdir
from os.path import isfile, join

# training, validation and testing directory (has to be modified according to each user)
train_img_dir_init = r"E:\Large Data\real_time_object\#Dataset\VisDrone\VisDrone2018-train\sequences" # raw text (\t, \a ignored)
train_annot_dir_init = train_img_dir_init + r"\annotations"
val_img_dir_init = r"E:\Large Data\real_time_object\#Dataset\VisDrone\VisDrone2018-val\sequences"
val_annot_dir_init = val_img_dir_init + r"\annotations"
test_img_dir_init = r"E:\Large Data\real_time_object\#Dataset\VisDrone\VisDrone2018-test\sequences"

train_img_dir = r"E:\Large Data\real_time_object\#Dataset\VisDrone\train_final"
train_annot_dir = train_img_dir+r"\annotations"
train_annot_file_init = "train_annotations_init.csv"
train_annot_file = "train_annotations.csv"

val_img_dir = r"E:\Large Data\real_time_object\#Dataset\VisDrone\val_final"
val_annot_dir = val_img_dir+r"\annotations"
val_annot_file_init = "val_annotations_init.csv"
val_annot_file = "val_annotations.csv"

test_img_dir = r"E:\Large Data\real_time_object\#Dataset\VisDrone\test_final"

''' the function maps each class id with their names respectively'''
def key_map(x):
    return {
        '0': 'Ignored Region',
        '1': 'Pedestrian',
        '2': 'People',
        '3': 'Bicycle',
        '4': 'Car',
        '5': 'Van',
        '6': 'Truck',
        '7': 'Tricycle',
        '8': 'Awning-tricycle',
        '9': 'Bus',
        '10': 'Motor',
        '11': 'Others',
    }.get(x, 11) # 11 is default if x not found

#print(key_map(s))


'''choose and save random 20 photoes from each sequence and rename them'''
def preprocessing_images(img_dir_init,img_dir_final):
    i=0
    for path, dirs, files in os.walk(img_dir_init):
        # print("----------")
        # print(path)
        # print(dirs)
        # print(files)
        # print("^^^^^^^^^")
        if i > 0:
            random.shuffle(files)
            files=files[0:20]
            for file in files:
                if os.path.basename(path) not in file:
                    os.rename(os.path.join(path,file),os.path.join(path,os.path.basename(path)+file))
                if os.path.basename(path) in file:
                    copyfile(os.path.join(path,file),os.path.join(img_dir_final,file))

        i=i+1
    return None
    


''' The fucntion reaname 
csv format : path/to/image.jpg,x1,y1,x2,y2,class_name'''

def preprocessing_annotations(annot_dir_init, annot_file_init):
    init = 1
    for filename in os.listdir(annot_dir_init):
        if filename.endswith(".txt"):    
            annot_file_init = filename.split('.')[0]
            rows =[]
            print(annot_file_init)
            with open(os.path.join(annot_dir_init, filename), 'r') as csvfile:
                csvreader = csv.reader(csvfile, delimiter = ',', lineterminator = '\n') 
                for row in csvreader:
                    rows.append(row)
                #print("Total no. of rows: %d"%(csvreader.line_num))
            #print("Total number of rows: %d"%(len(rows)))
            rows_final =[]
            #print(filename)
            for row in rows:
                if int(row[7]) == 0:
                    pass
                else:
                    if len(row[0]) == 1:
                        x = "000000"
                    elif len(row[0]) == 2:
                        x = "00000"
                    elif len(row[0]) == 3:
                        x = "0000"
                    elif len(row[0]) == 4:
                        x = "000"
                    else:
                        raise ValueError('A very specific bad thing happened')
                    rows_final.append(["../"+annot_file_init+ x +str(row[0])+".jpg",row[2],row[3],int(row[2])+int(row[4]),int(row[3])+int(row[5]),str(key_map(row[7]))])

            x = 'w'
            if init == 0:
                x = 'a'

            with open(os.path.join(annot_dir_final, annot_file_final), x, newline='') as csvfile:
                init = 0
                csvwriter = csv.writer(csvfile) 
                csvwriter.writerows(rows_final)
                
        else:
            pass                
    print("all annotations prepocessed!")
    return None



''' the function takes out random num_rows from csv_file and save it to csv_file_new '''
def filter_csv(img_path, csv_path, csv_file, csv_file_new):    # example: csv_path = annot_train_dir, csv_file = train_annot_file, num_rows = 2000
                                                               # num_rows = num of rows in new annotation file i.e. number of box bounded objects
    imgfiles = [f for f in listdir(img_path) if isfile(join(img_path, f))]

    rows=[]
    with open(os.path.join(csv_path, csv_file), 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter = ',', lineterminator = '\n')
        for row in csvreader:
            if (row[0][3:]) in imgfiles:
                rows.append(row)

    with open(os.path.join(csv_path, csv_file_new), 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerows(rows)

    return None


## invoke functions (in the order)

#preprocessing_annotations()
#preprocessing_images(test_img_dir_init,test_img_dir)
filter_csv(train_img_dir, train_annot_dir, train_annot_file_init, train_annot_file)