import cv2
import math
import numpy as np
import os
import glob
import json
import shutil
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element

def getRotatedImg(Pi_angle,img_path,img_write_path):
    img = cv2.imread(img_path)
    rows, cols = img.shape[:2]
    a, b = cols / 2, rows / 2
    M = cv2.getRotationMatrix2D((a, b), angle, 1)
    rotated_img = cv2.warpAffine(img, M, (cols, rows))  # 旋转后的图像保持大小不变
    cv2.imwrite(img_write_path,rotated_img)
    return a,b

def getRotatedAnno(Pi_angle,a,b,anno_path,anno_write_path):
    tree = ET.parse(anno_path)
    root = tree.getroot()
    objects = root.findall("object")
    for obj in objects:
        bbox = obj.find('bndbox')
        x1 = float(bbox.find('xmin').text) - 1
        y1 = float(bbox.find('ymin').text) - 1
        x2 = float(bbox.find('xmax').text) - 1
        y2 = float(bbox.find('ymax').text) - 1

        x3=x1
        y3=y2
        x4=x2
        y4=y1

        X1 = (x1 - a) * math.cos(Pi_angle) - (y1 - b) * math.sin(Pi_angle) + a
        Y1 = (x1 - a) * math.sin(Pi_angle) + (y1 - b) * math.cos(Pi_angle) + b

        X2 = (x2 - a) * math.cos(Pi_angle) - (y2 - b) * math.sin(Pi_angle) + a
        Y2 = (x2 - a) * math.sin(Pi_angle) + (y2 - b) * math.cos(Pi_angle) + b

        X3 = (x3 - a) * math.cos(Pi_angle) - (y3 - b) * math.sin(Pi_angle) + a
        Y3 = (x3 - a) * math.sin(Pi_angle) + (y3 - b) * math.cos(Pi_angle) + b

        X4 = (x4 - a) * math.cos(Pi_angle) - (y4 - b) * math.sin(Pi_angle) + a
        Y4 = (x4 - a) * math.sin(Pi_angle) + (y4 - b) * math.cos(Pi_angle) + b

        X_MIN=min(X1,X2,X3,X4)
        X_MAX = max(X1, X2, X3, X4)
        Y_MIN = min(Y1, Y2, Y3, Y4)
        Y_MAX = max(Y1, Y2, Y3, Y4)

        bbox.find('xmin').text=str(int(X_MIN))
        bbox.find('ymin').text=str(int(Y_MIN))
        bbox.find('xmax').text=str(int(X_MAX))
        bbox.find('ymax').text=str(int(Y_MAX))

    tree.write(anno_write_path)  # 保存修改后的XML文件

def rotate(angle,img_dir,anno_dir,img_write_dir,anno_write_dir):
    if not os.path.exists(img_write_dir):
        os.makedirs(img_write_dir)

    if not os.path.exists(anno_write_dir):
        os.makedirs(anno_write_dir)

    Pi_angle = -angle * math.pi / 180.0  # 弧度制，后面旋转坐标需要用到，注意负号！！！
    img_names=os.listdir(img_dir)
    for img_name in img_names:
        img_path=os.path.join(img_dir,img_name)
        img_write_path=os.path.join(img_write_dir,img_name[:-4]+'R'+str(angle)+'.jpg')
        #
        anno_path=os.path.join(anno_dir,img_name[:-4]+'.xml')
        anno_write_path = os.path.join(anno_write_dir, img_name[:-4]+'R'+str(angle)+'.xml')
        #
        a,b=getRotatedImg(Pi_angle,img_path,img_write_path)
        getRotatedAnno(Pi_angle,a,b,anno_path,anno_write_path)

angle=180
img_dir='several/JPEGImages'
anno_dir='several/Annotations'
img_write_dir='Rotated/rotated_JPEGImages'
anno_write_dir='Rotated/rotated_Annotations'

rotate(angle,img_dir,anno_dir,img_write_dir,anno_write_dir)