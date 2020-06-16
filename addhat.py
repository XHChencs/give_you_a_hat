# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 23:38:35 2020
"""

import paddlehub as hub
import tkinter as tk
from PIL import ImageTk,Image
from tkinter import filedialog
import os
import cv2
 

root = tk.Tk()
root.title('给你一顶圣诞帽')
root.geometry('600x600')
canvas=tk.Canvas(root,height=500,width=500)
canvas.pack()

# 添加圣诞帽
def add_hat(img_path, hat_path):
    # 加载人脸识别模型,取出关键点坐标
    model = hub.Module(name='ultra_light_fast_generic_face_detector_1mb_320')
    input_dict = {'image': [img_path]}
    results = model.face_detection(data=input_dict, visualization=True)
    for result in results:
        left, right, top, bottom = int(result['data'][0]['left']), int(result['data'][0]['right']),\
                                int(result['data'][0]['top']), int(result['data'][0]['bottom'])
    
    # 对帽子进行缩放
    hat=cv2.imread(hat_path)
    hat_h, hat_w, _ = hat.shape
    face_w = right - left

    ratio = face_w/hat_w
    resized_hat_h = int(round(hat_h*ratio))
    resized_hat_w = int(round(hat_w*ratio))
    resized_hat = cv2.resize(hat,(resized_hat_w,resized_hat_h))
    # 判断ROI是否超出边界
    while top-resized_hat_h<0:
        resized_hat = cv2.resize(resized_hat,(int(resized_hat_w*0.9),int(resized_hat_h*0.9)))
        resized_hat_h = resized_hat.shape[0]
        resized_hat_w = resized_hat.shape[1]
    # 读取人物照片
    person = cv2.imread(img_path)
    
    # 制作掩膜
    hat2gray = cv2.cvtColor(resized_hat, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
    ret, mask = cv2.threshold(hat2gray, 249, 255, cv2.THRESH_BINARY)  # 设置阈值，大于175的置为255，小于175的置为0
    mask_inv = cv2.bitwise_not(mask)
    
    # 掩膜
    mid_axis = int((right+left)/2)
    half_wide = int(resized_hat_w/2)
    roi = person[(top-resized_hat_h):top, (mid_axis-half_wide):(mid_axis-half_wide+resized_hat_w)]
    person_bg = cv2.bitwise_and(roi, roi, mask=mask)  #删除了ROI中的logo区域
    hat_fg = cv2.bitwise_and(resized_hat, resized_hat, mask=mask_inv) #删除了logo中的空白区域
    dst = cv2.add(person_bg, hat_fg)
    person[(top-resized_hat_h):top, (mid_axis-half_wide):(mid_axis-half_wide+resized_hat_w)] = dst 
    
    # 保存头像
    profile_path = 'your_profile_photo/'+os.path.basename(img_path)
    cv2.imwrite(profile_path, person)
    return profile_path
'''
img_path='profile_photo/1.jpeg'
hat_path='hat.jpg'

cv2.imshow("image", add_hat(img_path, hat_path))
cv2.waitKey(0)
'''
def gui():
    global image
    img_path = filedialog.askopenfilename() #获取文件路径
    hat_path = 'hat.jpg'
    profile_path = add_hat(img_path, hat_path)
    img = Image.open(profile_path)
    w,h = img.size
    mlength = max(w,h)
    ratio = 500/mlength
    w_new = int(w*ratio)
    h_new = int(h*ratio)
    re_img = img.resize((w_new,h_new))
    image = ImageTk.PhotoImage(re_img)
    canvas.create_image(260,260,anchor='center', image=image)  
    tk.messagebox.showinfo(title='Info', message='New profile photo has generated, please find it at the file: your_profile_photo')


b = tk.Button(root,text='Select your profile photo', command=gui)  #设置按钮，并给它openpicture命令
b.pack()
root.mainloop()

