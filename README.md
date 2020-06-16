# give_you_a_hat
Add a Christmas hat at your profile photo

## 环境配置
- python 3.6
- paddlehub 1.7.1
- PIL 7.1.2

## 代码说明
addhat.py是初代版本，当上传的图片无法识别出人脸时会奔溃  
addhatv2.py是针对第一代版本的改进

## 功能说明
- 用户可通过GUI界面选择自己头像的路径
- 程序可识别真人头像和漫画头像，生成的新的图片存放在`your_profile_photo`文件夹
- 若不能识别头像，则提醒用户更换头像

## 结果展示
选择图片界面
![界面1]('./results/1.png')
生成头像界面
![界面2]('./results/3.png')
无法识别头像时的提示
![界面3]('./results/5.png')
