import cv2
import math
import numpy as np
import os
import glob
import json
import shutil
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element

def h_MirrorImg(img_path,img_write_path):
    img = cv2.imread(img_path)
    mirror_img = cv2.flip(img, 1)  #
    cv2.imwrite(img_write_path,mirror_img)
def v_MirrorImg(img_path,img_write_path):
    img = cv2.imread(img_path)
    mirror_img = cv2.flip(img, 0)  #
    cv2.imwrite(img_write_path,mirror_img)
def a_MirrorImg(img_path,img_write_path):
    img = cv2.imread(img_path)
    mirror_img = cv2.flip(img, -1)  #
    cv2.imwrite(img_write_path,mirror_img)

def h_MirrorAnno(anno_path,anno_write_path):
    tree = ET.parse(anno_path)
    root = tree.getroot()
    size=root.find('size')
    w=int(size.find('width').text)
    objects = root.findall("object")
    for obj in objects:
        bbox = obj.find('bndbox')
        x1 = float(bbox.find('xmin').text)
        x2 = float(bbox.find('xmax').text)
        x1=w-x1+1
        x2=w-x2+1

        assert x1>0
        assert x2>0

        bbox.find('xmin').text=str(int(x2))
        bbox.find('xmax').text=str(int(x1))

    tree.write(anno_write_path)  # 保存修改后的XML文件
def v_MirrorAnno(anno_path,anno_write_path):
    tree = ET.parse(anno_path)
    root = tree.getroot()
    size = root.find('size')
    h=int(size.find('height').text)
    objects = root.findall("object")
    for obj in objects:
        bbox = obj.find('bndbox')
        y1 = float(bbox.find('ymin').text)
        y2 = float(bbox.find('ymax').text)

        y1=h-y1+1
        y2=h-y2+1

        assert y1>0
        assert y2>0

        bbox.find('ymin').text=str(int(y2))
        bbox.find('ymax').text=str(int(y1))

    tree.write(anno_write_path)  # 保存修改后的XML文件
def a_MirrorAnno(anno_path,anno_write_path):
    tree = ET.parse(anno_path)
    root = tree.getroot()
    size = root.find('size')
    w=int(size.find('width').text)
    h = int(size.find('height').text)
    objects = root.findall("object")
    for obj in objects:
        bbox = obj.find('bndbox')
        x1 = float(bbox.find('xmin').text)
        y1 = float(bbox.find('ymin').text)
        x2 = float(bbox.find('xmax').text)
        y2 = float(bbox.find('ymax').text)

        x1=w-x1+1
        x2=w-x2+1

        y1 = h - y1+1
        y2 = h - y2+1

        assert x1 > 0
        assert x2 > 0
        assert y1 > 0
        assert y2 > 0

        bbox.find('xmin').text=str(int(x2))
        bbox.find('xmax').text=str(int(x1))
        bbox.find('ymin').text=str(int(y2))
        bbox.find('ymax').text=str(int(y1))

    tree.write(anno_write_path)  # 保存修改后的XML文件
def mirror(img_dir,anno_dir,img_write_dir,anno_write_dir):
    if not os.path.exists(img_write_dir):
        os.makedirs(img_write_dir)

    if not os.path.exists(anno_write_dir):
        os.makedirs(anno_write_dir)
    img_names=os.listdir(img_dir)
    for img_name in img_names:
        img_path=os.path.join(img_dir,img_name)
        h_img_write_path=os.path.join(img_write_dir,img_name[:-4]+'h'+'.jpg')
        anno_path=os.path.join(anno_dir,img_name[:-4]+'.xml')
        h_anno_write_path = os.path.join(anno_write_dir, img_name[:-4]+'h'+'.xml')
        #
        v_img_write_path = os.path.join(img_write_dir, img_name[:-4] + 'v' + '.jpg')
        v_anno_write_path = os.path.join(anno_write_dir, img_name[:-4] + 'v' + '.xml')
        #
        a_img_write_path = os.path.join(img_write_dir, img_name[:-4] + 'a' + '.jpg')
        a_anno_write_path = os.path.join(anno_write_dir, img_name[:-4] + 'a' + '.xml')
        #
        h_MirrorImg(img_path,h_img_write_path)
        v_MirrorImg(img_path,v_img_write_path)
        a_MirrorImg(img_path, a_img_write_path)
        h_MirrorAnno(anno_path,h_anno_write_path)
        v_MirrorAnno(anno_path, v_anno_write_path)
        a_MirrorAnno(anno_path, a_anno_write_path)


img_dir='several/JPEGImages'
anno_dir='several/Annotations'
img_write_dir='Mirror/mirrored_JPEGImages'
anno_write_dir='Mirror/mirrored_Annotations'

mirror(img_dir,anno_dir,img_write_dir,anno_write_dir)
'''
imga=cv2.imread('14a.jpg')
imgh=cv2.imread('14h.jpg')
imgv=cv2.imread('14v.jpg')


cv2.rectangle(imga,(606,898),(855,1432),(0,255,0),4)
cv2.rectangle(imgh,(606,489),(855,1023),(0,255,0),4)
cv2.rectangle(imgv,(32,898),(281,1432),(0,255,0),4)
cv2.imwrite('a.jpg',imga)
cv2.imwrite('v.jpg',imgv)
cv2.imwrite('h.jpg',imgh)
'''
