import cv2
import math
img=cv2.imread('14h.jpg')
rows, cols = img.shape[:2]
##填充图像为正方形，而且要能保证填充后的图像在0到360°旋转的时候，原图像的像素不会损失
re=cv2.copyMakeBorder(img,int(cols/2),int(cols/2),int(rows/2),int(rows/2),cv2.BORDER_CONSTANT)

def getRotatedImg(Pi_angle,img_path,img_write_path):
    img = cv2.imread(img_path)
    rows, cols = img.shape[:2]
    a, b = cols / 2, rows / 2
    M = cv2.getRotationMatrix2D((a, b), angle, 1)
    rotated_img = cv2.warpAffine(img, M, (cols, rows))  # 旋转后的图像保持大小不变
    cv2.imwrite(img_write_path,rotated_img)

for angle in range(0,180,30):
    Pi_angle = -angle * math.pi / 180.0
    img_path='re.jpg'
    img_write_path=str(angle)+'.jpg'
    getRotatedImg(Pi_angle, img_path, img_write_path)

#验证是否标签被正确的改变
#for origin image: xmin:606 ymin:489 xmax:855 ymax:1023
cv2.rectangle(re,(606+int(rows/2),489+int(cols/2)),(855+int(rows/2),1023+int(cols/2)),(0,255,0),4)
#
def crop():
    pass