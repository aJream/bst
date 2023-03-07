## 半色调技术

半色调技术是一种将灰度图像转换为黑白图像的技术。它是通过将灰度图像的像素值映射到黑白像素值上来实现的。

比如说，在一块只能显示纯黑或纯白的屏幕上，如何将一张灰度图显示出灰度的效果，这时就可以用半色调技术实现。

如下，左边是一张灰度图，中间是使用半色调技术转换后输出的图像，右边是输出图像的局部放大



| 初始灰度图                                                   | 半色调转换后的输出图像                                       | 输出图像局部放大(使用win10自带【画图】软件打开放大)          |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![image-20230307153806255](https://gitcode.net/ajream/myimages/-/raw/master/pictures/2023/03/7_15_38_10_image-20230307153806255.png) | ![b_t](https://gitcode.net/ajream/myimages/-/raw/master/pictures/2023/03/7_15_38_38_b_t.jpg) | ![image-20230307154005805](https://gitcode.net/ajream/myimages/-/raw/master/pictures/2023/03/7_15_40_8_image-20230307154005805.png) |



## 原理

### 基本原理

我们都知道，一个像素点有0~255共256种灰度值，值越大图像越“白”，反之越“黑”。

对于一些屏幕，只能显示0或1（用1表示255）两种灰度值，也就是只能显示纯黑或纯白，这怎么办？

半色调技术实际是把一个像素点用一个矩阵块来表示，如果像素值比较大（越白），那么矩阵快白色部分就越多，如图所示：

![image-20230307160532625](https://gitcode.net/ajream/myimages/-/raw/master/pictures/2023/03/7_16_5_36_image-20230307160532625.png)







这个矩阵就是bayer矩阵，矩阵边长可以选择1，2，4，8，16，上图矩阵边长是2

如果是16，那么就可以表示16*16=256种灰度值了



如上图所示，对于边长为2的bayer矩阵，假如只有4种颜色值（0，1，2，3），如果像素值比0大，那么就把bayer矩阵的位置0设置为白色；如果比1大，就把位置<u>0和1</u>都设置为白色……

但实际上，灰度值有256种，因此bayer矩阵<u>需要乘以(256/(2*2))</u>，如下

![image-20230307162219466](https://gitcode.net/ajream/myimages/-/raw/master/pictures/2023/03/7_16_22_23_image-20230307162219466.png)

如果像素值比128大，那么0，64，128这3个位置都设置为白色



可以看出，假设输入图像边长为a，bayer矩阵边长为k，则输出图像的边长为a*k，即是输入图像的k倍



### bayer矩阵生成

![img](https://gitcode.net/ajream/myimages/-/raw/master/pictures/2023/03/7_16_30_45_20190908204513333.png.)



> 注意：整数*矩阵即矩阵的数乘运算，相当于矩阵每个元素都乘以一个整数

根据这个公式，可以写出一个代码：

```py
def getStandardMat(k):
    '''
    函数作用：获取bayer矩阵
    return：是否生成成功，成功的话同时返回numpy类型的矩阵
    k: 是bayer矩阵的阶数，取值一般为1 2 4 8 16
    '''
    if k & (k-1) != 0:
        return False, None
    if k == 1:
        return True, [[0.5]]
    m = [[0, 2], [3, 1]]
    m = np.array(m)
    while(m.shape[0] != k):
        m1 = np.zeros((m.shape[0]*2, m.shape[1]*2))
        m1[:m.shape[0], :m.shape[1]] += 4*m
        m1[:m.shape[0], m.shape[1]:] += 4*m+2
        m1[m.shape[0]:, :m.shape[1]] += 4*m+3
        m1[m.shape[0]:, m.shape[1]:] += 4*m+1
        m = m1
    return True, m
```

测试一下：

| ![image-20230307163826329](https://gitcode.net/ajream/myimages/-/raw/master/pictures/2023/03/7_16_38_30_image-20230307163826329.png) | ![image-20230307163903989](https://gitcode.net/ajream/myimages/-/raw/master/pictures/2023/03/7_16_39_7_image-20230307163903989.png) | ![image-20230307163929791](https://gitcode.net/ajream/myimages/-/raw/master/pictures/2023/03/7_16_39_34_image-20230307163929791.png) |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |





## 实践操作

该程序实现读取一张RGB图片，转为灰度图后再采用变色调技术转换图片

使用该程序只需要修改输入图片路径以及输出图片路径即可

```py
# 该文件实现半色调技术的代码

import cv2
import numpy as np

def getBayerMat(k):
    '''
    函数作用：获取bayer矩阵
    return：是否生成成功，成功的话同时返回numpy类型的矩阵
    k: 是bayer矩阵的阶数，取值一般为1 2 4 8 16
    '''
    if k & (k-1) != 0:
        return False, None
    if k == 1:
        return True, np.array([[0.5]])
    m = [[0, 2], [3, 1]]
    m = np.array(m)
    while(m.shape[0] != k):
        m1 = np.zeros((m.shape[0]*2, m.shape[1]*2))
        m1[:m.shape[0], :m.shape[1]] += 4*m
        m1[:m.shape[0], m.shape[1]:] += 4*m+2
        m1[m.shape[0]:, :m.shape[1]] += 4*m+3
        m1[m.shape[0]:, m.shape[1]:] += 4*m+1
        m = m1
    return True, m


def convertImg(img, k=4, f=False, useGray=False):
    '''
    k：bayer矩阵大小
    f：由于转换后图像尺寸会变大k倍，f表示是否先缩小k倍
    useGray：传入的img是否为灰度图
    '''
    if not useGray:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if f:
        img = cv2.resize(img, dsize=None, fx=1/k, fy=1/k)
    ret, bayers = getBayerMat(k)
    if not ret:
        print(f"矩阵阶数k={k}非2的倍数")
        return

    bayers *= (256//(k*k))
    h, w = img.shape
    newImg = np.zeros((k*h, k*w), dtype='uint8')
    
    # 遍历图像每个像素点
    for i in range(0, h, 1):
        for j in range(0, w, 1):
            # 对于每个像素点，遍历bayer矩阵，判断是否该把矩阵中某一位置设置为纯白(255)或纯黑(0)
            for p in range(k): 
                for q in range(k):
                    if img[i][j] > bayers[p][q]:
                        newImg[k*(i)+p][k*(j)+q] = 255
                    else:
                        newImg[k*(i)+p][k*(j)+q] = 0
    return newImg

if __name__ == '__main__':
    imgPath = r'D:\Users\xxx\Desktop\imgs\1-1.jpg'
    img = cv2.imread(imgPath, 0)  # 读取图片并转为灰度图
    nimg = convertImg(img, k=4, f=False, useGray=True)
    cv2.imwrite("../out/b2.png", nimg) # 输出转换后的图片


```





## 使用pyqt5做一个GUI操作界面

代码下载

需要安装的库

```
PyQt5                             5.15.0
opencv-python                     4.3.0.36
numpy                             1.19.0
```

![image-20230307170508261](https://gitcode.net/ajream/myimages/-/raw/master/pictures/2023/03/7_17_5_11_image-20230307170508261.png)

使用方法：

运行src/main.py文件即可

```sh
> python main.py
```

