# -*- coding:utf-8 -*-
 
 
from PIL import Image
import os
 
 
def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.png':  # 假设漫画全部都是png格式
                L.append(os.path.join(root, file))  # 输出为数组
    return L
 
 
def join(png1, png2, NewImageName, SavePath):
    img1, img2 = Image.open(png1), Image.open(png2)
    size1, size2 = img1.size, img2.size  # 获取两个图片长宽
    joint = Image.new('RGB', (size1[0]+size2[0], size1[1]))
    loc1, loc2 = (0, 0), (size1[0], 0)
    joint.paste(img2, loc1) #如需要左到右拼接，只要将img2改成img1，img1改成img2即可
    joint.paste(img1, loc2)
    joint.save('%s%s.png' % (SavePath,NewImageName))  # 输出
 
 
def main():
    ImgPath = input("图片文件夹位置(以/结尾)：")
    SavePath = input("拼接后图片存放的位置(以/结尾)：")
    image = file_name("ImgPath")  # 获取当前目录下指定文件
    j = 0
    for i in image:
            NewImage = "%s-%s"%(j+1,j) #拼接之后的图片的文件名
            join(image[j], image[j+1],NewImage,SavePath)  # 如果是第一次就直接两图合并
            j = j + 1

if __name__ == '__main__':
    main()
